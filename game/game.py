from __future__ import annotations

import random
from typing import Any

from game.data import (
    FINAL_LOCATION,
    HEAL_AMOUNT,
    LOCATIONS,
    MONSTER_DAMAGE,
    MONSTER_SCORE_REWARD,
    SHOP_POTION_COST,
    WIN_ITEM,
)
from game.location import Location
from game.player import Player


class Game:
    def __init__(self, player_name: str):
        self.player = Player(player_name)
        self._is_won = False
        self._won_reason = ""
        self.last_message = "Your adventure begins. Good luck!"
        self.cave_explored = False
        self.forest_searched = False
        self.monster_defeated = False

    @property
    def current_location(self) -> Location:
        return Location.from_id(self.player.current_location)

    @property
    def is_won(self) -> bool:
        return self._is_won

    @property
    def is_lost(self) -> bool:
        return self.player.is_dead()

    @property
    def is_finished(self) -> bool:
        return self.is_won or self.is_lost

    def to_dict(self) -> dict[str, Any]:
        return {
            "player": self.player.to_dict(),
            "is_won": self._is_won,
            "won_reason": self._won_reason,
            "last_message": self.last_message,
            "cave_explored": self.cave_explored,
            "forest_searched": self.forest_searched,
            "monster_defeated": self.monster_defeated,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Game":
        player_data = data["player"]
        game = cls(player_data["name"])
        game.player = Player.from_dict(player_data)
        game._is_won = bool(data.get("is_won", False))
        game._won_reason = str(data.get("won_reason", ""))
        game.last_message = str(data.get("last_message", ""))
        game.cave_explored = bool(data.get("cave_explored", False))
        game.forest_searched = bool(data.get("forest_searched", False))
        game.monster_defeated = bool(data.get("monster_defeated", False))
        return game

    def get_available_actions(self) -> list[dict]:
        if self.is_finished:
            return []
        actions = []
        for action in self.current_location.actions:
            aid = action["id"]
            if aid == "use_potion" and not self.player.has_item("potion"):
                continue
            if aid == "buy_potion" and self.player.score < SHOP_POTION_COST:
                continue
            if aid == "castle_use_key" and not self.player.has_item(WIN_ITEM):
                continue
            actions.append(action)
        move_castle = {
            "id": "move_castle",
            "label": "Journey to the Ancient Castle",
        }
        if self.player.current_location == "forest" and not any(
            a["id"] == "move_castle" for a in actions
        ):
            actions.insert(2, move_castle)
        return actions

    def do_action(self, action_id: str) -> dict[str, Any]:
        if self.is_finished:
            return self._result(
                message="The game is already over.",
            )
        valid_ids = {a["id"] for a in self.get_available_actions()}
        if action_id not in valid_ids:
            return self._result(
                message=f"You cannot do that here: {action_id}.",
            )
        handler = getattr(self, f"_act_{action_id}", None)
        if handler is None:
            return self._result(message=f"Nothing happened for {action_id}.")
        return handler()

    def _result(self, message: str) -> dict[str, Any]:
        self.last_message = message
        return {
            "message": message,
            "is_won": self.is_won,
            "is_lost": self.is_lost,
            "is_finished": self.is_finished,
            "player": self.player.to_dict(),
            "current_location": self.player.current_location,
        }

    def _move_to(self, location_id: str, message: str) -> dict[str, Any]:
        if location_id not in LOCATIONS:
            return self._result(message="Unknown destination.")
        self.player.current_location = location_id
        loc = Location.from_id(location_id)
        return self._result(message=f"{message} You are now at {loc.name}.")

    def _act_move_village(self) -> dict[str, Any]:
        return self._move_to("village", "You walk back along the path.")

    def _act_move_forest(self) -> dict[str, Any]:
        return self._move_to("forest", "You head into the dense trees.")

    def _act_move_cave(self) -> dict[str, Any]:
        return self._move_to("cave", "You step into the cold darkness of the cave.")

    def _act_move_castle(self) -> dict[str, Any]:
        return self._move_to(
            "castle",
            "You travel beyond the forest, across the hills, to the castle gates.",
        )

    def _act_visit_shop(self) -> dict[str, Any]:
        return self._move_to("shop", "You push the door open and step inside.")

    def _act_buy_potion(self) -> dict[str, Any]:
        if self.player.score < SHOP_POTION_COST:
            return self._result(
                message=f"You need at least {SHOP_POTION_COST} score to buy a potion."
            )
        self.player.score -= SHOP_POTION_COST
        self.player.add_item("potion")
        return self._result(
            message=f"You bought a Healing Potion for {SHOP_POTION_COST} score points."
        )

    def _act_check_inventory(self) -> dict[str, Any]:
        inv = self.player.inventory
        if not inv:
            return self._result(message="Your inventory is empty.")
        summary = ", ".join(sorted(set(f"{i} (x{inv.count(i)})" if inv.count(i) > 1 else i for i in set(inv))))
        return self._result(message=f"Inventory: {summary}.")

    def _act_use_potion(self) -> dict[str, Any]:
        if not self.player.has_item("potion"):
            return self._result(message="You don't have any potions.")
        self.player.remove_item("potion")
        healed = self.player.heal(HEAL_AMOUNT)
        return self._result(
            message=f"You drank the Healing Potion and recovered {healed} health points."
        )

    def _act_forest_search(self) -> dict[str, Any]:
        if not self.forest_searched:
            self.forest_searched = True
            self.player.score += 10
            reward = random.choice(["map", "potion"])
            self.player.add_item(reward)
            return self._result(
                message=(
                    f"You searched the forest carefully and found a {reward}! "
                    f"+10 score."
                )
            )
        self.player.score += 5
        return self._result(
            message="You search the forest again. Nothing new, but you gain +5 score for your effort."
        )

    def _act_cave_explore(self) -> dict[str, Any]:
        if not self.cave_explored:
            self.cave_explored = True
            if not self.player.has_item(WIN_ITEM):
                self.player.add_item(WIN_ITEM)
                self.player.score += 30
            return self._result(
                message=(
                    "You explore the cave carefully and find a glowing golden "
                    f"{WIN_ITEM} hidden behind a stone! +30 score."
                )
            )
        return self._result(
            message="You already explored this part of the cave. The key is in your pocket."
        )

    def _act_cave_fight(self) -> dict[str, Any]:
        if self.monster_defeated:
            return self._result(
                message="The monster has already been defeated. There is nothing more to fight here."
            )
        self.monster_defeated = True
        self.player.take_damage(MONSTER_DAMAGE)
        if self.player.is_dead():
            return self._result(
                message="The monster was too strong! You collapse... Your adventure ends here."
            )
        self.player.score += MONSTER_SCORE_REWARD
        if not self.player.has_item("sword"):
            self.player.add_item("sword")
            return self._result(
                message=(
                    f"You defeated the cave monster! You took {MONSTER_DAMAGE} damage "
                    f"but earned the Hero's Sword and +{MONSTER_SCORE_REWARD} score!"
                )
            )
        return self._result(
            message=(
                f"You defeated the cave monster! You took {MONSTER_DAMAGE} damage "
                f"and earned +{MONSTER_SCORE_REWARD} score!"
            )
        )

    def _act_castle_use_key(self) -> dict[str, Any]:
        if not self.player.has_item(WIN_ITEM):
            return self._result(message="The gate is locked. You need the Castle Key.")
        if self.player.current_location != FINAL_LOCATION:
            return self._result(message="There is no castle gate here.")
        self._is_won = True
        self._won_reason = (
            f"{self.player.name} unlocked the Ancient Castle with the Castle Key "
            "and claimed the legendary treasure!"
        )
        self.player.score += 100
        return self._result(message=self._won_reason)

    def __repr__(self) -> str:
        return (
            f"Game(player={self.player!r}, is_won={self.is_won}, "
            f"is_lost={self.is_lost})"
        )
