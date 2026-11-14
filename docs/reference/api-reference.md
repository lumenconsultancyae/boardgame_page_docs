# API & Operator Reference Guide

## 1. Environment Configuration

| Variable | Default | Description |
| :--- | :--- | :--- |
| `BOARDGAME_APP_HOST` | `0.0.0.0` | Bind address for the HTTP application server. |
| `BOARDGAME_APP_PORT` | `8088` | Listening TCP port for HTTP requests. |
| `BOARDGAME_DB_PATH` | `data/boardgames.sqlite3` | Filesystem path to the SQLite database file (or `:memory:`). |
| `BOARDGAME_SEED_DEFAULTS` | `true` | Whether to seed starter board games, play sessions, and UAE events when tables are empty. |
| `BOARDGAME_ENVIRONMENT` | `development` | Runtime environment label (`development`, `test`, `production`). |

---

## 2. REST API Endpoints (`/api/v1`)

### Health Check
- **`GET /api/v1/health`**
  - Returns `200 OK`: `{"status": "ok", "service": "boardgame-page", "version": "1.0.0"}`

### Board Game Catalog
- **`GET /api/v1/games`**
  - Optional query parameters: `status` (`owned|wishlist|played`), `players` (`int`), `max_playtime` (`int`), `max_complexity` (`float`), `mechanic` (`str`), `search` (`str`), `include_archived` (`true|false`).
  - Returns `200 OK`: `{"items": [Game, ...], "total": int}`
- **`POST /api/v1/games`**
  - Creates a new board game entry. Returns `201 Created` with the persisted `Game` object.
- **`GET /api/v1/games/{game_id}`**
  - Returns `200 OK` with `Game` or `404 Not Found`.
- **`PATCH /api/v1/games/{game_id}`**
  - Updates `status`, `rating`, `complexity_weight`, `title`, `subtitle`, or `archived`. Returns `200 OK`.
- **`DELETE /api/v1/games/{game_id}`**
  - Removes a board game. Returns `200 OK`: `{"deleted_id": game_id, "status": "deleted"}`.

### Visual Rule Summaries & Flowcharts
- **`GET /api/v1/games/{game_id}/rules-diagram`**
  - Returns `200 OK` with setup steps, turn phases, scoring rules, quick tips, `mermaid_code` (`flowchart LR`), interactive `diagram_nodes` / `diagram_edges`, and `whatsapp_share`.

### Play Session Tracker
- **`GET /api/v1/sessions`**
  - Optional query parameter: `game_id`. Returns `200 OK`: `{"items": [PlaySession, ...], "total": int}`.
- **`POST /api/v1/sessions`**
  - Logs a play session (`game_id`, `players`, `winner`, `duration_mins`, `location`, `scores`, `notes`) and increments the parent game's `play_count`. Returns `201 Created`.

### Collection Analytics & Graphs
- **`GET /api/v1/analytics`**
  - Returns `200 OK` with `complexity_distribution`, `mechanics_breakdown`, `category_breakdown`, `player_count_coverage`, and `top_played_games`.

### UAE Boardgame Events
- **`GET /api/v1/events`**
  - Optional query parameters: `emirate`, `category`, `search`. Returns `200 OK`: `{"items": [UaeEvent, ...], "total": int}`.
- **`POST /api/v1/events`**
  - Publishes a new UAE boardgame event. Returns `201 Created`.
- **`GET /api/v1/events/{event_id}`**
  - Returns `200 OK` with `UaeEvent` or `404 Not Found`.
- **`POST /api/v1/events/{event_id}/rsvp`**
  - Increments `rsvp_count` by `1` (returns `400 Bad Request` if `rsvp_count >= max_players`).
- **`DELETE /api/v1/events/{event_id}`**
  - Deletes a UAE event by ID. Returns `200 OK`.

### WhatsApp Sharing Endpoints
- **`GET /api/v1/share/whatsapp/game/{game_id}`**
  - Returns `200 OK`: `{"game_id": ..., "title": ..., "text": ..., "whatsapp_url": "https://wa.me/?text=..."}`
- **`GET /api/v1/share/whatsapp/list`**
  - Accepts all `/api/v1/games` filter parameters plus `title`. Returns `200 OK` with formatted list text and `whatsapp_url`.
- **`GET /api/v1/share/whatsapp/event/{event_id}`**
  - Returns `200 OK` with formatted UAE event invite text and `whatsapp_url`.

---

## 3. Standard Error Envelope

All domain validation (`400`) and resource lookup (`404`) errors return a consistent JSON structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid game status 'borrowed'. Must be one of: owned, played, wishlist.",
    "details": {
      "field": "status",
      "allowed": ["owned", "played", "wishlist"]
    }
  }
}
```
