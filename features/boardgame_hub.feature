@e2e
Feature: Boardgame Hub Collection Tracker, Rule Diagrams, Analytics, WhatsApp Sharing, and UAE Events
  As a boardgame enthusiast and game night host in the UAE
  I want to track my boardgame collection and play sessions, generate visual rule diagrams, share summaries on WhatsApp, and track UAE boardgame events
  So that my friends can easily learn game rules, pick games for game night, and join community meetups

  Scenario: Browse and filter the boardgame collection and log a play session
    Given I open the Boardgame Hub web application
    When I filter the collection by status "owned", player count "4", and max duration "90"
    Then the collection catalog displays matching owned 4-player games including "Catan"
    And the browser URL query parameters reflect status "owned", player count "4", and max duration "90"
    When I add a new board game titled "Cascadia Test Game" with complexity "1.9", playtime "25", mechanics "Tile Placement, Pattern Building", and setup steps "Place starter habitat tile; Deal 4 wildlife tokens"
    Then "Cascadia Test Game" appears in the board game catalog
    When I log a play session for "Cascadia Test Game" won by "Zayd Al-Mansoor" with players "Khalid, Zayd Al-Mansoor, Omar" and scores "Zayd Al-Mansoor: 94, Khalid: 88, Omar: 81" at "Unwind Cafe Dubai"
    Then the recent play log lists the session won by "Zayd Al-Mansoor" with score "Zayd Al-Mansoor: 94"
    When I open the visual rule diagram for "Cascadia Test Game"
    Then the setup checklist contains "Place starter habitat tile"

  Scenario: Inspect visual rule summaries and interactive setup and turn-order diagrams
    Given I open the Boardgame Hub web application
    When I open the visual rule diagram for "Catan"
    Then the interactive SVG rule flowchart is displayed with setup, turn phase, and scoring nodes
    When I click on turn phase node "node_phase_2" in the rule flowchart
    Then the phase inspector displays the rule summary for "Phase 2: Domestic & Maritime Trade"
    And the setup checklist and exportable Mermaid v11 flowchart syntax are populated

  Scenario: View collection analytics graphs and complexity distribution
    Given I open the Boardgame Hub web application
    When I navigate to the "analytics" workspace tab
    Then the collection analytics KPIs and complexity weight distribution graph are displayed
    And the core game mechanics graph and most-played games leaderboard are rendered

  Scenario: Generate and preview WhatsApp share messages for game rules and curated game lists
    Given I open the Boardgame Hub web application
    When I trigger WhatsApp sharing for the filtered boardgame list
    Then the WhatsApp share drawer opens with a formatted game list message and a valid wa.me deep link
    When I copy the formatted WhatsApp message to the clipboard
    Then a confirmation toast "WhatsApp message copied to clipboard!" is displayed
    When I close the WhatsApp share drawer and open the rule diagram for "Wingspan"
    And I trigger WhatsApp sharing for the active game rule summary
    Then the WhatsApp share drawer opens with a formatted rule summary for "Wingspan" and a valid wa.me deep link

  Scenario: Discover, filter, host, RSVP, and share UAE boardgame events on WhatsApp
    Given I open the Boardgame Hub web application
    When I navigate to the "events" workspace tab
    And I filter UAE boardgame events by emirate "Dubai"
    Then all displayed UAE events are located in "Dubai"
    When I host a new UAE boardgame event titled "JLT Strategy Meetup Test" in "Dubai" at "JLT Community Hub"
    Then "JLT Strategy Meetup Test" is listed in the UAE events board
    When I RSVP to the UAE event "JLT Strategy Meetup Test"
    Then the RSVP seat counter for "JLT Strategy Meetup Test" increments by 1
    When I trigger WhatsApp sharing for the UAE event "JLT Strategy Meetup Test"
    Then the WhatsApp share drawer opens with a formatted event invite for "JLT Strategy Meetup Test" and a valid wa.me deep link
