"""Selenium Page Object encapsulating all DOM interactions for Boardgame Hub."""

from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BoardgameHubPage:
    """Driver-isolated Page Object for Boardgame Hub workflows."""

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        self._driver = driver
        self._base_url = base_url
        self._wait = WebDriverWait(
            driver,
            timeout,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        )

    def open_home(self) -> None:
        self._driver.get(f"{self._base_url}/")
        self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="game-card"]')))

    def switch_tab(self, tab_name: str) -> None:
        btn = self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="tab-{tab_name}"]'))
        )
        btn.click()
        self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="view-{tab_name}"]')))

    def filter_collection(self, status: str, players: str, max_playtime: str = "") -> None:
        status_el = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="filter-status"]'))
        )
        Select(status_el).select_by_value(status)
        players_el = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="filter-players"]'))
        )
        Select(players_el).select_by_value(players)
        if max_playtime:
            playtime_el = self._wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="filter-playtime"]'))
            )
            Select(playtime_el).select_by_value(max_playtime)
        self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="game-card"]')))

    def get_current_url(self) -> str:
        return self._driver.current_url

    def get_visible_game_titles(self) -> list[str]:
        def _read_titles(drv: WebDriver) -> list[str]:
            cards = drv.find_elements(By.CSS_SELECTOR, '[data-testid="game-card"] .game-card-title')
            return [c.text.strip() for c in cards if c.text.strip()]

        return self._wait.until(_read_titles)

    def add_game(
        self,
        title: str,
        complexity: str,
        mechanics: str,
        playtime: str = "60",
        setup_steps: str = "",
    ) -> None:
        self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-toggle-add-game"]'))
        ).click()
        title_input = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="game-title-input"]'))
        )
        title_input.clear()
        title_input.send_keys(title)

        playtime_input = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="game-playtime-input"]')
        playtime_input.clear()
        playtime_input.send_keys(playtime)

        comp_input = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="game-complexity-input"]')
        comp_input.clear()
        comp_input.send_keys(complexity)

        mech_input = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="game-mechanics-input"]')
        mech_input.clear()
        mech_input.send_keys(mechanics)

        if setup_steps:
            setup_input = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="game-setup-input"]')
            setup_input.clear()
            setup_input.send_keys(setup_steps)

        self._driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-submit-game"]').click()
        self._wait.until(
            lambda d: title in [el.text.strip() for el in d.find_elements(By.CSS_SELECTOR, ".game-card-title")]
        )

    def log_play_session(
        self,
        game_title: str,
        winner: str,
        players: str,
        location: str,
        scores: str = "",
    ) -> None:
        self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-toggle-log-session"]'))
        ).click()
        game_select = Select(
            self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="session-game-input"]')))
        )
        for opt in game_select.options:
            if game_title in opt.text:
                game_select.select_by_visible_text(opt.text)
                break

        p_in = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="session-players-input"]')
        p_in.clear()
        p_in.send_keys(players)

        w_in = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="session-winner-input"]')
        w_in.clear()
        w_in.send_keys(winner)

        if scores:
            s_in = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="session-scores-input"]')
            s_in.clear()
            s_in.send_keys(scores)

        loc_in = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="session-location-input"]')
        loc_in.clear()
        loc_in.send_keys(location)

        self._driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-submit-session"]').click()
        self._wait.until(
            lambda d: winner.lower() in d.find_element(By.CSS_SELECTOR, '[data-testid="sessions-list"]').text.lower()
        )

    def get_sessions_log_text(self) -> str:
        return self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="sessions-list"]'))
        ).text

    def open_rule_diagram_for_game(self, game_title: str) -> None:
        self.switch_tab("rules")
        sel_el = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="rules-game-select"]'))
        )
        sel = Select(sel_el)
        for opt in sel.options:
            if game_title in opt.text:
                sel.select_by_visible_text(opt.text)
                break
        self._wait.until(
            lambda d: game_title in d.find_element(By.CSS_SELECTOR, '[data-testid="rules-diagram-title"]').text
        )

    def has_svg_flowchart_nodes(self) -> bool:
        svg = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="rules-svg-diagram"] svg'))
        )
        nodes = svg.find_elements(By.CSS_SELECTOR, "g[data-testid^='diagram-node-']")
        return len(nodes) >= 3

    def click_flowchart_node(self, node_id: str) -> None:
        node = self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="diagram-node-{node_id}"]'))
        )
        node.click()

    def get_node_inspector_text(self) -> str:
        return self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="rules-node-inspector"]'))
        ).text

    def get_setup_steps_count(self) -> int:
        items = self._driver.find_elements(By.CSS_SELECTOR, '[data-testid="rules-setup-list"] li')
        return len(items)

    def get_setup_steps_text(self) -> str:
        return self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="rules-setup-list"]'))
        ).text

    def get_mermaid_code_text(self) -> str:
        el = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="rules-mermaid-code"]')
        return el.get_attribute("textContent") or ""

    def is_analytics_rendered(self) -> dict[str, bool]:
        self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="analytics-kpis"] .kpi-card')))
        return {
            "kpis": len(self._driver.find_elements(By.CSS_SELECTOR, '[data-testid="analytics-kpis"] .kpi-card')) >= 4,
            "complexity": len(self._driver.find_elements(By.CSS_SELECTOR, '#chart-complexity-bars .bar-row')) == 3,
            "mechanics": len(self._driver.find_elements(By.CSS_SELECTOR, '#chart-mechanics-bars .bar-row')) >= 1,
            "top_played": len(self._driver.find_elements(By.CSS_SELECTOR, '#chart-top-played-bars .bar-row')) >= 1,
        }

    def click_share_filtered_list_whatsapp(self) -> None:
        self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-share-list-whatsapp"]'))
        ).click()
        self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="whatsapp-share-drawer"]'))
        )

    def click_share_rules_whatsapp(self) -> None:
        self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-rules-whatsapp"]'))
        ).click()
        self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="whatsapp-share-drawer"]'))
        )

    def get_whatsapp_drawer_state(self) -> dict[str, str]:
        preview = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="whatsapp-preview-text"]'))
        )
        link = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="link-open-whatsapp"]')
        return {
            "text": preview.text,
            "href": link.get_attribute("href") or "",
        }

    def close_whatsapp_drawer_if_open(self) -> None:
        drawers = self._driver.find_elements(By.CSS_SELECTOR, '[data-testid="whatsapp-share-drawer"]')
        if drawers and drawers[0].is_displayed():
            self._driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-close-whatsapp-drawer"]').click()

    def click_copy_whatsapp_message(self) -> None:
        self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-copy-whatsapp"]'))
        ).click()

    def get_toast_banner_text(self) -> str:
        return self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="toast-banner"]'))
        ).text

    def click_share_event_whatsapp(self, event_title: str) -> None:
        for card in self._driver.find_elements(By.CSS_SELECTOR, '[data-testid="event-card"]'):
            if event_title in card.text:
                card.find_element(By.CSS_SELECTOR, '[data-testid="btn-share-event-whatsapp"]').click()
                break
        self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="whatsapp-share-drawer"]'))
        )

    def filter_events_by_emirate(self, emirate: str) -> None:
        sel_el = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="filter-emirate"]'))
        )
        Select(sel_el).select_by_value(emirate)
        self._wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="event-card"]')))

    def get_visible_event_emirates(self) -> list[str]:
        badges = self._driver.find_elements(By.CSS_SELECTOR, '[data-testid="event-card"] .emirate-badge')
        return [b.text.strip() for b in badges if b.text.strip()]

    def create_uae_event(self, title: str, emirate: str, venue: str) -> None:
        self._wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-toggle-add-event"]'))
        ).click()
        t_in = self._wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="event-title-input"]'))
        )
        t_in.clear()
        t_in.send_keys(title)

        Select(self._driver.find_element(By.CSS_SELECTOR, '[data-testid="event-emirate-input"]')).select_by_value(
            emirate
        )

        v_in = self._driver.find_element(By.CSS_SELECTOR, '[data-testid="event-venue-input"]')
        v_in.clear()
        v_in.send_keys(venue)

        self._driver.find_element(By.CSS_SELECTOR, '[data-testid="btn-submit-event"]').click()
        self._wait.until(
            lambda d: title in [el.text.strip() for el in d.find_elements(By.CSS_SELECTOR, '[data-testid="event-card"] .game-card-title')]
        )

    def get_event_rsvp_count(self, event_title: str) -> int:
        def _lookup(drv: WebDriver) -> int:
            for card in drv.find_elements(By.CSS_SELECTOR, '[data-testid="event-card"]'):
                if event_title in card.text:
                    pill = card.find_element(By.CSS_SELECTOR, '[data-testid="event-rsvp-pill"]').text
                    # Format: "RSVPs: 1/16"
                    num_part = pill.split("RSVPs:")[-1].strip().split("/")[0]
                    return int(num_part)
            return -1

        return self._wait.until(lambda d: _lookup(d) if _lookup(d) >= 0 else False)

    def click_rsvp_for_event(self, event_title: str) -> None:
        before_cnt = self.get_event_rsvp_count(event_title)
        for card in self._driver.find_elements(By.CSS_SELECTOR, '[data-testid="event-card"]'):
            if event_title in card.text:
                card.find_element(By.CSS_SELECTOR, '[data-testid="btn-event-rsvp"]').click()
                break
        self._wait.until(lambda _d: self.get_event_rsvp_count(event_title) == before_cnt + 1)
