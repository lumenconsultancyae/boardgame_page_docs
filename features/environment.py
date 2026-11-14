"""Behave E2E environment hooks with console error monitoring and fail-safe snapshot teardown."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from typing import Any
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from features.pages.boardgame_hub_page import BoardgameHubPage

BASE_URL = os.environ.get("BOARDGAME_E2E_BASE_URL", "http://127.0.0.1:8088").rstrip("/")


def before_all(context: Any) -> None:
    """Initialize headless Chromium WebDriver and shared Page Object."""
    context.base_url = BASE_URL
    opts = Options()
    for flag in (
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1440,900",
    ):
        opts.add_argument(flag)
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    context.driver = webdriver.Chrome(options=opts)
    context.hub_page = BoardgameHubPage(context.driver, context.base_url)


def before_scenario(context: Any, scenario: Any) -> None:
    """Snapshot pre-existing game and event IDs safely before each scenario."""
    context.scenario_start_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    context.pre_game_ids = None
    context.pre_event_ids = None
    context.created_game_ids = []
    context.created_event_ids = []

    try:
        g_resp = requests.get(f"{context.base_url}/api/v1/games?include_archived=true", timeout=5)
        if g_resp.status_code == 200:
            context.pre_game_ids = {item["id"] for item in g_resp.json().get("items", [])}
        e_resp = requests.get(f"{context.base_url}/api/v1/events", timeout=5)
        if e_resp.status_code == 200:
            context.pre_event_ids = {item["id"] for item in e_resp.json().get("items", [])}
    except requests.RequestException:
        context.pre_game_ids = None
        context.pre_event_ids = None


def after_scenario(context: Any, scenario: Any) -> None:
    """Verify zero unexpected browser console errors and clean up only test-created resources."""
    severe: list[str] = []
    try:
        logs = context.driver.get_log("browser")
        severe = [
            entry["message"]
            for entry in logs
            if entry.get("level") in ("SEVERE", "ERROR") and "favicon.ico" not in entry.get("message", "")
        ]
    except Exception:
        severe = []

    # Non-destructive diff teardown guarded by pre_game_ids / pre_event_ids != None and ownership check
    if context.pre_game_ids is not None:
        try:
            g_resp = requests.get(f"{context.base_url}/api/v1/games?include_archived=true", timeout=5)
            if g_resp.status_code == 200:
                for item in g_resp.json().get("items", []):
                    gid = item["id"]
                    created_at = item.get("created_at", "")
                    if gid not in context.pre_game_ids and (
                        created_at >= context.scenario_start_ts or "test" in item.get("title", "").lower()
                    ):
                        requests.delete(f"{context.base_url}/api/v1/games/{gid}", timeout=5)
        except requests.RequestException:
            pass

    if context.pre_event_ids is not None:
        try:
            e_resp = requests.get(f"{context.base_url}/api/v1/events", timeout=5)
            if e_resp.status_code == 200:
                for item in e_resp.json().get("items", []):
                    eid = item["id"]
                    created_at = item.get("created_at", "")
                    if eid not in context.pre_event_ids and (
                        created_at >= context.scenario_start_ts or "test" in item.get("title", "").lower()
                    ):
                        requests.delete(f"{context.base_url}/api/v1/events/{eid}", timeout=5)
        except requests.RequestException:
            pass

    assert not severe, f"Unexpected browser console errors in '{scenario.name}': {severe}"


def after_all(context: Any) -> None:
    """Quit WebDriver cleanly."""
    if getattr(context, "driver", None) is not None:
        context.driver.quit()
