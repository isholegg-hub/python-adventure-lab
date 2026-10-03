import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game.game import Game
from game.data import MONSTER_DAMAGE, MONSTER_SCORE_REWARD, SHOP_POTION_COST, HEAL_AMOUNT


class TestGameCreation:
    def test_current_location_village(self):
        g = Game("Alice")
        assert g.player.current_location == "village"
        assert g.current_location.id == "village"

    def test_player_name(self):
        g = Game("Bob")
        assert g.player.name == "Bob"

    def test_initial_flags(self):
        g = Game("Charlie")
        assert g.is_won is False
        assert g.is_lost is False
        assert g.is_finished is False
        assert g.cave_explored is False
        assert g.monster_defeated is False


class TestMoveActions:
    def test_move_village_forest(self):
        g = Game("Hero")
        result = g.do_action("move_forest")
        assert g.player.current_location == "forest"
        assert result["current_location"] == "forest"

    def test_move_forest_village(self):
        g = Game("Hero")
        g.do_action("move_forest")
        assert g.player.current_location == "forest"
        g.do_action("move_village")
        assert g.player.current_location == "village"

    def test_move_forest_cave(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        assert g.player.current_location == "cave"

    def test_move_castle_not_available_from_village(self):
        g = Game("Hero")
        actions = g.get_available_actions()
        action_ids = {a["id"] for a in actions}
        assert "move_castle" not in action_ids
        result = g.do_action("move_castle")
        assert "cannot do that here" in result["message"]

    def test_move_castle_available_from_forest(self):
        g = Game("Hero")
        g.do_action("move_forest")
        actions = g.get_available_actions()
        action_ids = {a["id"] for a in actions}
        assert "move_castle" in action_ids

    def test_move_castle_to_castle(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_castle")
        assert g.player.current_location == "castle"


class TestCaveExplore:
    def test_cave_explore_gives_key_and_score(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        initial_score = g.player.score
        result = g.do_action("cave_explore")
        assert g.player.has_item("key")
        assert g.player.score == initial_score + 30
        assert g.cave_explored is True

    def test_cave_explore_second_call_no_duplicate_key(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        g.do_action("cave_explore")
        key_count_before = g.player.count_item("key")
        score_before = g.player.score
        g.do_action("cave_explore")
        assert g.player.count_item("key") == key_count_before
        assert g.player.score == score_before


class TestCaveFight:
    def test_cave_fight_gives_sword_and_score_damage(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        initial_health = g.player.health
        initial_score = g.player.score
        result = g.do_action("cave_fight")
        assert g.player.has_item("sword")
        assert g.player.health == initial_health - MONSTER_DAMAGE
        assert g.player.score == initial_score + MONSTER_SCORE_REWARD
        assert g.monster_defeated is True

    def test_cave_fight_death_is_lost(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        g.player.health = 10
        result = g.do_action("cave_fight")
        assert g.player.is_dead()
        assert g.is_lost is True
        assert g.is_finished is True

    def test_cave_fight_second_call_monster_defeated(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        g.do_action("cave_fight")
        health_before = g.player.health
        score_before = g.player.score
        result = g.do_action("cave_fight")
        assert "already been defeated" in result["message"]
        assert g.player.health == health_before
        assert g.player.score == score_before


class TestWinPath:
    def test_win_path_full(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        g.do_action("cave_explore")
        assert g.player.has_item("key")
        g.player.current_location = "castle"
        score_before = g.player.score
        result = g.do_action("castle_use_key")
        assert g.is_won is True
        assert g.is_finished is True
        assert g.player.score == score_before + 100

    def test_win_path_via_move_castle(self):
        g = Game("Hero")
        g.do_action("move_forest")
        g.do_action("move_cave")
        g.do_action("cave_explore")
        g.do_action("move_forest")
        g.do_action("move_castle")
        assert g.player.current_location == "castle"
        result = g.do_action("castle_use_key")
        assert g.is_won is True


class TestUsePotion:
    def test_use_potion_heals_and_removes(self):
        g = Game("Hero")
        g.player.take_damage(50)
        g.player.add_item("potion")
        health_before = g.player.health
        assert g.player.count_item("potion") == 1
        result = g.do_action("use_potion")
        assert g.player.health == min(100, health_before + HEAL_AMOUNT)
        assert g.player.count_item("potion") == 0

    def test_use_potion_not_available_when_none(self):
        g = Game("Hero")
        g.player.take_damage(50)
        actions = g.get_available_actions()
        action_ids = {a["id"] for a in actions}
        assert "use_potion" not in action_ids


class TestBuyPotion:
    def test_buy_potion_insufficient_score_do_action_blocked(self):
        g = Game("Hero")
        g.player.score = SHOP_POTION_COST - 1
        g.do_action("visit_shop")
        score_before = g.player.score
        potion_count_before = g.player.count_item("potion")
        result = g.do_action("buy_potion")
        assert "cannot do that here" in result["message"]
        assert g.player.score == score_before
        assert g.player.count_item("potion") == potion_count_before

    def test_buy_potion_insufficient_score_handler_guard(self):
        g = Game("Hero")
        g.player.score = SHOP_POTION_COST - 1
        g.do_action("visit_shop")
        score_before = g.player.score
        potion_count_before = g.player.count_item("potion")
        result = g._act_buy_potion()
        assert "need at least" in result["message"]
        assert g.player.score == score_before
        assert g.player.count_item("potion") == potion_count_before

    def test_buy_potion_success(self):
        g = Game("Hero")
        g.player.score = SHOP_POTION_COST + 20
        g.do_action("visit_shop")
        score_before = g.player.score
        result = g.do_action("buy_potion")
        assert g.player.score == score_before - SHOP_POTION_COST
        assert g.player.count_item("potion") == 1

    def test_buy_potion_not_available_when_poor(self):
        g = Game("Hero")
        g.player.score = 0
        g.do_action("visit_shop")
        actions = g.get_available_actions()
        action_ids = {a["id"] for a in actions}
        assert "buy_potion" not in action_ids


class TestGameSerialization:
    def test_to_dict_from_dict_round_trip(self):
        g1 = Game("Hero")
        g1.do_action("move_forest")
        g1.do_action("move_cave")
        g1.do_action("cave_explore")
        g1.do_action("cave_fight")
        g1.do_action("move_forest")
        g1.player.score = 999
        d = g1.to_dict()
        g2 = Game.from_dict(d)
        assert g2.player.name == g1.player.name
        assert g2.player.health == g1.player.health
        assert g2.player.score == g1.player.score
        assert g2.player.inventory == g1.player.inventory
        assert g2.player.current_location == g1.player.current_location
        assert g2.is_won == g1.is_won
        assert g2.is_lost == g1.is_lost
        assert g2.cave_explored == g1.cave_explored
        assert g2.monster_defeated == g1.monster_defeated
        assert g2.last_message == g1.last_message

    def test_to_dict_from_dict_won_state(self):
        g1 = Game("Winner")
        g1._is_won = True
        g1._won_reason = "Test win reason"
        g1.cave_explored = True
        g1.forest_searched = True
        g1.monster_defeated = True
        d = g1.to_dict()
        g2 = Game.from_dict(d)
        assert g2.is_won is True
        assert g2.cave_explored is True
        assert g2.forest_searched is True
        assert g2.monster_defeated is True

    def test_from_dict_defaults(self):
        d = {
            "player": {"name": "Test", "health": 100, "score": 0, "inventory": [], "current_location": "village"},
        }
        g = Game.from_dict(d)
        assert g.is_won is False
        assert g.cave_explored is False
        assert g.forest_searched is False
        assert g.monster_defeated is False
