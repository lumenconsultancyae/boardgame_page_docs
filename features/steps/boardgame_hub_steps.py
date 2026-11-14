"""Behave step definitions and assertions for Boardgame Hub E2E verification."""

from __future__ import annotations

from typing import Any
from behave import given, then, when


@given("I open the Boardgame Hub web application")
def step_open_app(context: Any) -> None:
    context.hub_page.open_home()


@when('I filter the collection by status "{status}", player count "{players}", and max duration "{max_playtime}"')
def step_filter_collection(context: Any, status: str, players: str, max_playtime: str) -> None:
    context.hub_page.filter_collection(status=status, players=players, max_playtime=max_playtime)


@then('the collection catalog displays matching owned 4-player games including "{expected_game}"')
def step_verify_filtered_catalog(context: Any, expected_game: str) -> None:
    titles = context.hub_page.get_visible_game_titles()
    assert expected_game in titles, f"Expected '{expected_game}' in filtered titles {titles}"


@then('the browser URL query parameters reflect status "{status}", player count "{players}", and max duration "{max_playtime}"')
def step_verify_url_filter_params(context: Any, status: str, players: str, max_playtime: str) -> None:
    url = context.hub_page.get_current_url()
    assert f"status={status}" in url, f"Expected status={status} in {url}"
    assert f"players={players}" in url, f"Expected players={players} in {url}"
    assert f"max_playtime={max_playtime}" in url, f"Expected max_playtime={max_playtime} in {url}"


@when(
    'I add a new board game titled "{title}" with complexity "{complexity}", playtime "{playtime}", mechanics "{mechanics}", and setup steps "{setup_steps}"'
)
def step_add_new_game(
    context: Any,
    title: str,
    complexity: str,
    playtime: str,
    mechanics: str,
    setup_steps: str,
) -> None:
    context.hub_page.add_game(
        title=title,
        complexity=complexity,
        mechanics=mechanics,
        playtime=playtime,
        setup_steps=setup_steps,
    )


@then('"{title}" appears in the board game catalog')
def step_verify_game_in_catalog(context: Any, title: str) -> None:
    titles = context.hub_page.get_visible_game_titles()
    assert title in titles, f"Expected '{title}' in {titles}"


@when(
    'I log a play session for "{game_title}" won by "{winner}" with players "{players}" and scores "{scores}" at "{location}"'
)
def step_log_session(
    context: Any,
    game_title: str,
    winner: str,
    players: str,
    scores: str,
    location: str,
) -> None:
    context.hub_page.log_play_session(
        game_title=game_title,
        winner=winner,
        players=players,
        location=location,
        scores=scores,
    )


@then('the recent play log lists the session won by "{winner}" with score "{expected_score}"')
def step_verify_session_winner(context: Any, winner: str, expected_score: str) -> None:
    log_text = context.hub_page.get_sessions_log_text()
    assert winner.lower() in log_text.lower(), f"Expected winner '{winner}' in '{log_text}'"
    assert expected_score in log_text, f"Expected score '{expected_score}' in '{log_text}'"


@then('the setup checklist contains "{expected_step}"')
def step_verify_custom_setup_step(context: Any, expected_step: str) -> None:
    setup_text = context.hub_page.get_setup_steps_text()
    assert expected_step in setup_text, f"Expected '{expected_step}' in '{setup_text}'"


@when('I open the visual rule diagram for "{game_title}"')
def step_open_rule_diagram(context: Any, game_title: str) -> None:
    context.hub_page.open_rule_diagram_for_game(game_title)


@then("the interactive SVG rule flowchart is displayed with setup, turn phase, and scoring nodes")
def step_verify_svg_flowchart(context: Any) -> None:
    assert context.hub_page.has_svg_flowchart_nodes() is True


@when('I click on turn phase node "{node_id}" in the rule flowchart')
def step_click_flowchart_node(context: Any, node_id: str) -> None:
    context.hub_page.click_flowchart_node(node_id)


@then('the phase inspector displays the rule summary for "{expected_label}"')
def step_verify_phase_inspector(context: Any, expected_label: str) -> None:
    inspector_text = context.hub_page.get_node_inspector_text()
    assert expected_label in inspector_text, f"Expected '{expected_label}' in '{inspector_text}'"


@then("the setup checklist and exportable Mermaid v11 flowchart syntax are populated")
def step_verify_setup_and_mermaid(context: Any) -> None:
    assert context.hub_page.get_setup_steps_count() >= 2
    mermaid = context.hub_page.get_mermaid_code_text()
    assert mermaid.startswith("flowchart LR")


@when('I navigate to the "{tab_name}" workspace tab')
def step_navigate_tab(context: Any, tab_name: str) -> None:
    context.hub_page.switch_tab(tab_name)


@then("the collection analytics KPIs and complexity weight distribution graph are displayed")
def step_verify_analytics_kpis_and_complexity(context: Any) -> None:
    state = context.hub_page.is_analytics_rendered()
    assert state["kpis"] is True
    assert state["complexity"] is True


@then("the core game mechanics graph and most-played games leaderboard are rendered")
def step_verify_mechanics_and_leaderboard(context: Any) -> None:
    state = context.hub_page.is_analytics_rendered()
    assert state["mechanics"] is True
    assert state["top_played"] is True


@when("I trigger WhatsApp sharing for the filtered boardgame list")
def step_share_list_whatsapp(context: Any) -> None:
    context.hub_page.click_share_filtered_list_whatsapp()


@then("the WhatsApp share drawer opens with a formatted game list message and a valid wa.me deep link")
def step_verify_whatsapp_list_drawer(context: Any) -> None:
    drawer = context.hub_page.get_whatsapp_drawer_state()
    assert "My Boardgame List" in drawer["text"]
    assert drawer["href"].startswith("https://wa.me/?text=")


@when("I copy the formatted WhatsApp message to the clipboard")
def step_copy_whatsapp_message(context: Any) -> None:
    context.hub_page.click_copy_whatsapp_message()


@then('a confirmation toast "{expected_toast}" is displayed')
def step_verify_toast_message(context: Any, expected_toast: str) -> None:
    toast = context.hub_page.get_toast_banner_text()
    assert expected_toast in toast, f"Expected '{expected_toast}' in '{toast}'"


@when('I close the WhatsApp share drawer and open the rule diagram for "{game_title}"')
def step_close_drawer_and_open_rules(context: Any, game_title: str) -> None:
    context.hub_page.close_whatsapp_drawer_if_open()
    context.hub_page.open_rule_diagram_for_game(game_title)


@when("I trigger WhatsApp sharing for the active game rule summary")
def step_share_rules_whatsapp(context: Any) -> None:
    context.hub_page.click_share_rules_whatsapp()


@then('the WhatsApp share drawer opens with a formatted rule summary for "{game_title}" and a valid wa.me deep link')
def step_verify_whatsapp_rules_drawer(context: Any, game_title: str) -> None:
    drawer = context.hub_page.get_whatsapp_drawer_state()
    assert game_title in drawer["text"]
    assert "Turn Flow" in drawer["text"]
    assert drawer["href"].startswith("https://wa.me/?text=")


@when('I filter UAE boardgame events by emirate "{emirate}"')
def step_filter_uae_events(context: Any, emirate: str) -> None:
    context.hub_page.filter_events_by_emirate(emirate)


@then('all displayed UAE events are located in "{emirate}"')
def step_verify_event_emirates(context: Any, emirate: str) -> None:
    emirates = context.hub_page.get_visible_event_emirates()
    assert len(emirates) >= 1
    assert all(e == emirate for e in emirates)


@when('I host a new UAE boardgame event titled "{title}" in "{emirate}" at "{venue}"')
def step_host_uae_event(context: Any, title: str, emirate: str, venue: str) -> None:
    context.hub_page.create_uae_event(title=title, emirate=emirate, venue=venue)


@then('"{title}" is listed in the UAE events board')
def step_verify_event_listed(context: Any, title: str) -> None:
    rsvp_cnt = context.hub_page.get_event_rsvp_count(title)
    assert rsvp_cnt >= 0
    context.last_rsvp_count = rsvp_cnt


@when('I RSVP to the UAE event "{title}"')
def step_rsvp_event(context: Any, title: str) -> None:
    context.last_rsvp_count = context.hub_page.get_event_rsvp_count(title)
    context.hub_page.click_rsvp_for_event(title)


@then('the RSVP seat counter for "{title}" increments by 1')
def step_verify_rsvp_incremented(context: Any, title: str) -> None:
    new_cnt = context.hub_page.get_event_rsvp_count(title)
    assert new_cnt == context.last_rsvp_count + 1


@when('I trigger WhatsApp sharing for the UAE event "{title}"')
def step_share_event_whatsapp(context: Any, title: str) -> None:
    context.hub_page.click_share_event_whatsapp(title)


@then('the WhatsApp share drawer opens with a formatted event invite for "{title}" and a valid wa.me deep link')
def step_verify_whatsapp_event_drawer(context: Any, title: str) -> None:
    drawer = context.hub_page.get_whatsapp_drawer_state()
    assert title in drawer["text"], f"Expected '{title}' in '{drawer['text']}'"
    assert drawer["href"].startswith("https://wa.me/?text=")
