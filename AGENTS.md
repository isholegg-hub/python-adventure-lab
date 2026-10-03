# Python Adventure Lab — AI Agent Instructions
## Purpose
Educational browser adventure game (Python + Flask). Teaches Python->OOP->Flask->Web transition via a playable Village→Forest→Cave→Castle quest. First project in a library of beginner IT projects.

## Project Structure
python-adventure-lab/
  app.py                 — Flask routes/session only. NO game logic here.
  game/
    __init__.py
    player.py            — Player class: health, score, inventory, location.
    location.py          — Location class from data dict.
    game.py              — Game core. Actions, transitions, win/lose, serialize.
    data.py              — Game world data dict (LOCATIONS, ITEMS, constants).
  templates/             — Jinja2 templates base/index/game/result.
  static/style.css       — Offline responsive CSS. No CDN.
  tests/                 — pytest (test_player.py, test_game.py).
  docs/uk/, docs/en/     — Ukrainian + English docs, lesson, vocabulary.

## Rules for Changing Code
- ALWAYS separate logic vs web: game logic in game/, Flask plumbing only in app.py. Never write rules for win/lose/damage/score in app.py.
- Use simple classes, avoid over-engineering. Small functions/methods, PEP 8, Python 3.11+.
- No database, no auth, no JS framework, no Bootstrap CDN in Version 1.
- No secrets in code. Use SECRET_KEY via env.

## Commands
Setup:
  python -m venv .venv
  .venv\Scripts\activate (Windows) or source .venv/bin/activate (*nix)
  pip install -r requirements.txt
Run:
  python app.py           # or flask run --debug (http://127.0.0.1:5000)
Test:
  pytest -v

## Architectural Constraints
- State via Flask session (Game.to_dict/from_dict). Allow future swap for PostgreSQL.
- HTTP: GET for reads (/, /game, /result). POST for mutations (/start, /action).
- Templates: pure Jinja, no JS framework. All actions via HTML <form method=POST>.

## Future Roadmap (V1 is current)
V1: Python + Flask + Session (done)
V2: PostgreSQL persistence
V3: REST API endpoints
V4: JavaScript / React front-end
V5: User authentication
V6: Docker containerization
V7: CI/CD pipeline + deploy
