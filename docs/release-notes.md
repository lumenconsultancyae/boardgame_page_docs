# Release Notes

## Version 1.0.0 (2026-11-13)

### New Capabilities

- **Board Game Collection & Play Session Tracker**:
  - Added full catalog management for Owned, Wishlist, and Played board games with player count bounds, playtime, complexity weight (`1.0–5.0`), mechanics, categories, and personal ratings.
  - Added play session logging with date, duration, café/venue location, players, winner badge, and session notes, automatically incrementing each game's play count.
- **Visual Rule Summaries & Interactive Turn-Order Diagrams**:
  - Added interactive SVG setup and turn-order flowcharts with clickable step inspection, 3-column rule cheat-sheets (Table Setup Checklist, Turn Phases, Scoring & First-Game Teach Tips), and exportable Mermaid v11 `flowchart LR` syntax.
- **Shareable Game Lists & Collection Analytics Graphs**:
  - Added multi-dimensional collection filtering (status, player count, max complexity, search) and visual analytics bar graphs for Complexity Weight Distribution, Player-Count Coverage, Core Mechanics Frequency, and Most-Played Games.
- **WhatsApp Sharing Integration**:
  - Added one-click WhatsApp message generation (`https://wa.me/?text=...` deep links + formatted preview + clipboard copy) for game rule summaries, filtered game lists, and UAE community event invites.
- **UAE Boardgame Events Hub**:
  - Added event discovery, Emirate filtering (Dubai, Abu Dhabi, Sharjah, Ajman, Ras Al Khaimah, Fujairah, Umm Al Quwain), event publishing, and live seat RSVP tracking.

### Known Gaps & Proposed Next Steps

- **BoardGameGeek (BGG) XML API Import**:
  - *Proposed Solution / Next Steps*: Add an optional infrastructure client adapter implementing a `CatalogImportPort` to fetch metadata by BGG Thing ID while keeping local SQLite caching as the primary source of truth.
