# Python Adventure Lab

## Overview

Python Adventure Lab is a small educational project that teaches Python, object-oriented programming, and Flask by building a playable browser adventure game. You start in a Village, journey through a Forest and Cave, find the Castle Key, and unlock the Ancient Castle. The project deliberately keeps game logic (pure Python classes) separated from the web layer (Flask routes + Jinja templates) so students can clearly trace the mental path: Python basics → software logic → Flask → a real Web App.

## Audience

Designed for kids around 10–14, teenagers, and adult beginners who know a little Python and want their first "real" project. Also useful for teachers as a first serious Python + Flask assignment. A full playthrough takes about 5–10 minutes.

## Tech Stack

- Python 3.11+
- Flask 3
- Jinja2 templates
- pytest
- Pure HTML + hand-written CSS
- No database, no JavaScript framework, no Bootstrap CDN, no external fonts

## Setup & Run

For the complete Windows, macOS, and Linux instructions, including Python setup, package installation, testing, and troubleshooting, see the [Setup, Run, and Build Guide](setup.md). This Flask project has no separate compile step.

## How to Play

Enter your name on the start screen. From the Village, go to the Forest. Enter the Cave, then **Explore the cave carefully** to find the Castle Key, and optionally **Fight the monster** (gain a Sword and score, but lose HP). Return to the Forest and choose **Journey to the Ancient Castle**. Finally, at the Castle, select **Use the Castle Key** to win. You can visit the Village Shop to buy Healing Potions with your Score. If your HP drops to zero, it's Game Over.

## Project Structure

```
python-adventure-lab/
  app.py                 — Flask entry point: routes, session, rendering. No game logic.
  requirements.txt       — Python dependencies (Flask, pytest, python-dotenv)
  .env.example           — Template for SECRET_KEY and other env vars
  .gitignore             — Git ignore rules
  AGENTS.md              — Agent instructions, architecture constraints, roadmap
  game/
    __init__.py          — Package marker for the game module
    data.py              — Game world data: LOCATIONS, ITEMS, and tuning constants
    player.py            — Player class: health, score, inventory, location logic
    location.py          — Location class that wraps entries from the data dict
    game.py              — Game core: actions, transitions, win/lose, serialize/deserialize
  templates/
    base.html            — Base Jinja2 layout (head, body wrapper)
    index.html           — Start screen with name input
    game.html            — Main gameplay screen: stats, location, action buttons
    result.html          — Win / Game Over screen with final score
  static/
    style.css            — Hand-written responsive CSS (offline, no CDN)
  tests/
    __init__.py          — Package marker for tests
    test_player.py       — Unit tests for the Player class
    test_game.py         — Unit tests for the Game class and actions
```

## Learning Levels

### Level 1 — Python Basics

Covers variables, `if`/`else`, lists, dicts, loops, and functions. Suggested exercises:

1. Change the player's starting HP in `game/player.py`.
2. Add a new item (e.g., a Shield) to `ITEMS` in `game/data.py` and wire it into an action.
3. Add a new location (e.g., a River crossing) to `LOCATIONS` in `game/data.py` with its own actions.
4. Add a new simple action (e.g., "Rest in the Village" that restores a bit of health).

### Level 2 — Python OOP

Covers classes, objects, attributes, methods, and `self`. Suggested exercises:

1. Create a new typed Item class (instead of plain strings) with `name`, `description`, and `effect`.
2. Add an NPC class for the Shop merchant and dialog lines.
3. Extract the Cave monster into an Enemy class with its own HP and attack logic.
4. Build a small interaction system so items, NPCs, and enemies can reference each other.

### Level 3 — Flask

Covers routes, GET/POST, `request`, `session`, Jinja, and HTML forms. Suggested exercises:

1. Add a new page, for example an `/about` or `/help` page with game instructions.
2. Wire a brand-new gameplay action through `/action` and verify it updates the session.
3. Add a new form (for example, "Choose your hero class" on the start screen).
4. Tweak the stats UI in `templates/game.html` — add progress bars, colors, or icons for HP / Score / Inventory.

### Level 4 — Advanced Ideas

Once the base project feels comfortable, explore real-world directions:

- Persist saves to **PostgreSQL** instead of Flask session.
- Expose gameplay through a **REST API** (`/api/action`, `/api/state`).
- Add **user accounts** and authentication.
- Rewrite the front end with **JavaScript / AJAX** so actions don't require a page reload.
- Add a **leaderboard** stored in the database.
- Support multiple selectable adventures (multi-adventure launcher).
- Add a simple **admin panel** to tune items and locations without editing code.

## Extending the Project (Roadmap)

- **V1** — Python + Flask + Session (current version)
- **V2** — PostgreSQL persistence for saved games
- **V3** — REST API endpoints for game state and actions
- **V4** — JavaScript / React front-end with AJAX calls
- **V5** — User authentication and per-account saves
- **V6** — Docker containerization for consistent deployments
- **V7** — CI/CD pipeline + automated deploy to a cloud host

## Running Tests

```bash
pytest -v
```
