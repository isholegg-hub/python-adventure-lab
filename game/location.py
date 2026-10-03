from typing import Any

from game.data import LOCATIONS


class Location:
    def __init__(self, location_id: str, data: dict[str, Any]):
        self.id = location_id
        self.name = data["name"]
        self.description = data["description"]
        self.actions = list(data.get("actions", []))

    def get_action(self, action_id: str) -> dict | None:
        for action in self.actions:
            if action["id"] == action_id:
                return action
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "actions": list(self.actions),
        }

    @classmethod
    def from_id(cls, location_id: str) -> "Location":
        if location_id not in LOCATIONS:
            raise KeyError(f"Unknown location: {location_id}")
        return cls(location_id, LOCATIONS[location_id])

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, name={self.name!r})"
