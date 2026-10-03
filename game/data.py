LOCATIONS = {
    "village": {
        "name": "Village",
        "description": (
            "A small peaceful village at the edge of the kingdom. "
            "Smoke rises from the chimneys, and the villagers go about their day. "
            "A winding path leads into the forest, and there is a small shop nearby."
        ),
        "actions": [
            {"id": "move_forest", "label": "Go to Forest"},
            {"id": "visit_shop", "label": "Visit Shop"},
            {"id": "check_inventory", "label": "Check Inventory"},
            {"id": "use_potion", "label": "Use Potion (if you have one)"},
        ],
    },
    "forest": {
        "name": "Forest",
        "description": (
            "A dense green forest. Sunlight barely reaches the ground through the tall pines. "
            "You hear birds singing and leaves rustling. "
            "One path goes back to the village, another leads into a dark cave."
        ),
        "actions": [
            {"id": "forest_search", "label": "Search the forest"},
            {"id": "move_village", "label": "Go back to Village"},
            {"id": "move_cave", "label": "Enter Cave"},
            {"id": "check_inventory", "label": "Check Inventory"},
            {"id": "use_potion", "label": "Use Potion (if you have one)"},
        ],
    },
    "cave": {
        "name": "Cave",
        "description": (
            "A cold, dark cave. Water drips from the ceiling somewhere deep inside. "
            "Your footsteps echo. You sense you are not alone — there might be treasure, "
            "and there might be danger."
        ),
        "actions": [
            {"id": "cave_explore", "label": "Explore the cave carefully"},
            {"id": "cave_fight", "label": "Fight the monster"},
            {"id": "move_forest", "label": "Return to Forest"},
            {"id": "check_inventory", "label": "Check Inventory"},
            {"id": "use_potion", "label": "Use Potion (if you have one)"},
        ],
    },
    "shop": {
        "name": "Village Shop",
        "description": (
            "A cozy little shop run by an old merchant. Shelves are lined with useful things: "
            "potions, maps, tools. The merchant greets you warmly."
        ),
        "actions": [
            {"id": "buy_potion", "label": "Buy a Healing Potion (costs 10 score)"},
            {"id": "move_village", "label": "Leave Shop and return to Village"},
            {"id": "check_inventory", "label": "Check Inventory"},
            {"id": "use_potion", "label": "Use Potion (if you have one)"},
        ],
    },
    "castle": {
        "name": "Ancient Castle",
        "description": (
            "You stand before an ancient stone castle. The gates are closed with a huge iron lock. "
            "Legends say that whoever opens the castle with the golden key wins the adventure — "
            "and the treasure hidden inside."
        ),
        "actions": [
            {"id": "castle_use_key", "label": "Use the Castle Key"},
            {"id": "move_cave", "label": "Go back to Cave"},
            {"id": "check_inventory", "label": "Check Inventory"},
            {"id": "use_potion", "label": "Use Potion (if you have one)"},
        ],
    },
}

ITEMS = {
    "key": {"name": "Castle Key", "description": "A shiny golden key that opens the castle gate."},
    "potion": {"name": "Healing Potion", "description": "Restores 40 health points when used."},
    "sword": {"name": "Hero's Sword", "description": "A magical sword, reward for defeating a monster."},
    "map": {"name": "Old Map", "description": "A crumpled map that shows a shortcut through the forest."},
}

WIN_ITEM = "key"
FINAL_LOCATION = "castle"
HEAL_AMOUNT = 40
MONSTER_DAMAGE = 35
MONSTER_SCORE_REWARD = 50
SHOP_POTION_COST = 10
