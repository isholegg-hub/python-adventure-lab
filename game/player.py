from game.data import HEAL_AMOUNT


class Player:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.score = 0
        self.inventory = []
        self.current_location = "village"

    def take_damage(self, amount: int) -> None:
        if amount <= 0:
            return
        self.health = max(0, self.health - amount)

    def heal(self, amount: int = HEAL_AMOUNT) -> int:
        if amount <= 0:
            return 0
        old_health = self.health
        self.health = min(100, self.health + amount)
        return self.health - old_health

    def add_item(self, item: str) -> None:
        self.inventory.append(item)

    def remove_item(self, item: str) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def count_item(self, item: str) -> int:
        return self.inventory.count(item)

    def is_dead(self) -> bool:
        return self.health <= 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
            "score": self.score,
            "inventory": list(self.inventory),
            "current_location": self.current_location,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        player = cls(data["name"])
        player.health = data["health"]
        player.score = data["score"]
        player.inventory = list(data.get("inventory", []))
        player.current_location = data.get("current_location", "village")
        return player

    def __repr__(self) -> str:
        return (
            f"Player(name={self.name!r}, health={self.health}, score={self.score}, "
            f"inventory={self.inventory}, location={self.current_location!r})"
        )
