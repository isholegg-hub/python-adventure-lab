import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game.player import Player


class TestPlayerCreation:
    def test_name(self):
        p = Player("Alice")
        assert p.name == "Alice"

    def test_default_health(self):
        p = Player("Bob")
        assert p.health == 100

    def test_default_score(self):
        p = Player("Charlie")
        assert p.score == 0

    def test_empty_inventory(self):
        p = Player("Dave")
        assert p.inventory == []

    def test_default_location(self):
        p = Player("Eve")
        assert p.current_location == "village"


class TestTakeDamage:
    def test_take_damage_30(self):
        p = Player("Hero")
        p.take_damage(30)
        assert p.health == 70

    def test_take_damage_200_not_negative(self):
        p = Player("Hero")
        p.take_damage(200)
        assert p.health == 0

    def test_take_damage_zero(self):
        p = Player("Hero")
        p.take_damage(0)
        assert p.health == 100

    def test_take_damage_negative(self):
        p = Player("Hero")
        p.take_damage(-10)
        assert p.health == 100


class TestHeal:
    def test_heal_20_from_70(self):
        p = Player("Hero")
        p.take_damage(30)
        assert p.health == 70
        healed = p.heal(20)
        assert p.health == 90
        assert healed == 20

    def test_heal_500_capped_at_100(self):
        p = Player("Hero")
        p.take_damage(30)
        healed = p.heal(500)
        assert p.health == 100
        assert healed == 30

    def test_heal_zero_no_change(self):
        p = Player("Hero")
        p.take_damage(30)
        healed = p.heal(0)
        assert p.health == 70
        assert healed == 0

    def test_heal_negative_no_change(self):
        p = Player("Hero")
        p.take_damage(30)
        healed = p.heal(-10)
        assert p.health == 70
        assert healed == 0


class TestInventory:
    def test_add_item(self):
        p = Player("Hero")
        p.add_item("key")
        assert "key" in p.inventory

    def test_has_item_true(self):
        p = Player("Hero")
        p.add_item("potion")
        assert p.has_item("potion") is True

    def test_has_item_false(self):
        p = Player("Hero")
        assert p.has_item("sword") is False

    def test_remove_item_true(self):
        p = Player("Hero")
        p.add_item("sword")
        result = p.remove_item("sword")
        assert result is True
        assert "sword" not in p.inventory

    def test_remove_item_false(self):
        p = Player("Hero")
        result = p.remove_item("key")
        assert result is False

    def test_add_multiple_items(self):
        p = Player("Hero")
        p.add_item("key")
        p.add_item("potion")
        p.add_item("sword")
        assert p.has_item("key")
        assert p.has_item("potion")
        assert p.has_item("sword")

    def test_count_item_single(self):
        p = Player("Hero")
        p.add_item("potion")
        assert p.count_item("potion") == 1

    def test_count_item_multiple(self):
        p = Player("Hero")
        p.add_item("potion")
        p.add_item("potion")
        p.add_item("potion")
        assert p.count_item("potion") == 3

    def test_count_item_none(self):
        p = Player("Hero")
        assert p.count_item("key") == 0


class TestIsDead:
    def test_is_dead_false_at_100(self):
        p = Player("Hero")
        assert p.is_dead() is False

    def test_is_dead_false_at_1(self):
        p = Player("Hero")
        p.take_damage(99)
        assert p.is_dead() is False

    def test_is_dead_true_at_0(self):
        p = Player("Hero")
        p.take_damage(100)
        assert p.is_dead() is True


class TestSerialization:
    def test_to_dict_structure(self):
        p = Player("Hero")
        p.take_damage(20)
        p.score = 50
        p.add_item("key")
        p.current_location = "forest"
        d = p.to_dict()
        assert d["name"] == "Hero"
        assert d["health"] == 80
        assert d["score"] == 50
        assert d["inventory"] == ["key"]
        assert d["current_location"] == "forest"

    def test_from_dict_round_trip(self):
        p1 = Player("Hero")
        p1.take_damage(25)
        p1.score = 75
        p1.add_item("potion")
        p1.add_item("sword")
        p1.current_location = "cave"
        d = p1.to_dict()
        p2 = Player.from_dict(d)
        assert p2.name == "Hero"
        assert p2.health == 75
        assert p2.score == 75
        assert p2.inventory == ["potion", "sword"]
        assert p2.current_location == "cave"

    def test_from_dict_empty_inventory(self):
        p1 = Player("Test")
        d = p1.to_dict()
        p2 = Player.from_dict(d)
        assert p2.inventory == []

    def test_from_dict_default_location(self):
        d = {"name": "Test", "health": 100, "score": 0, "inventory": []}
        p = Player.from_dict(d)
        assert p.current_location == "village"
