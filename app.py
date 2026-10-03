from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

from game.game import Game

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "dev-secret-key-change-me-in-production-32chars!"
    )
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/start", methods=["POST"])
    def start():
        name = (request.form.get("name") or "Hero").strip()
        if not name:
            name = "Hero"
        game = Game(name[:30])
        session["game_state"] = game.to_dict()
        return redirect(url_for("game_view"))

    @app.route("/game", methods=["GET"])
    def game_view():
        game = _restore_game()
        if game is None:
            return redirect(url_for("index"))
        if game.is_finished:
            return redirect(url_for("result"))
        location = game.current_location
        return render_template(
            "game.html",
            player=game.player.to_dict(),
            location=location.to_dict(),
            actions=game.get_available_actions(),
            last_message=game.last_message,
        )

    @app.route("/action", methods=["POST"])
    def action():
        game = _restore_game()
        if game is None:
            return redirect(url_for("index"))
        action_id = (request.form.get("action") or "").strip()
        if action_id:
            game.do_action(action_id)
        session["game_state"] = game.to_dict()
        if game.is_finished:
            return redirect(url_for("result"))
        return redirect(url_for("game_view"))

    @app.route("/result", methods=["GET"])
    def result():
        game = _restore_game()
        if game is None:
            return redirect(url_for("index"))
        if not game.is_finished:
            return redirect(url_for("game_view"))
        is_won = game.is_won
        final_message = (
            game.last_message
            if game.last_message
            else ("You conquered the adventure!" if is_won else "Your adventure ended.")
        )
        return render_template(
            "result.html",
            is_won=is_won,
            final_message=final_message,
            score=game.player.score,
            inventory=list(game.player.inventory),
        )

    def _restore_game() -> Game | None:
        state = session.get("game_state")
        if state is None:
            return None
        try:
            return Game.from_dict(state)
        except (KeyError, TypeError, ValueError):
            session.pop("game_state", None)
            return None

    return app


app = create_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") in {"1", "true", "True", "yes"}
    app.run(host="127.0.0.1", port=5000, debug=debug)
