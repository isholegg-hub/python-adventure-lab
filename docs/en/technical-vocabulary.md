# Technical Vocabulary

### Class
- **English**: A blueprint in Python that defines the structure and behavior of a type of thing. It bundles data (attributes) and functions (methods) together.
- **Українською**: Клас
- **Example**: The `Player` class in `game/player.py` defines how every player object stores health, score, and inventory.

### Object
- **English**: A concrete instance of a class. When you create a class as a blueprint, an object is one real thing built from that blueprint with its own values.
- **Українською**: Об'єкт
- **Example**: When a player enters "Alice" on the start screen, the app creates a `Player` object named Alice with 100 HP and 0 score.

### Attribute
- **English**: A piece of data stored inside an object. Attributes are variables that belong to a specific instance or class.
- **Українською**: Атрибут
- **Example**: `self.health` and `self.score` are two attributes of every `Player` object.

### Method
- **English**: A function that is defined inside a class and operates on objects of that class. It usually reads or modifies the object's attributes.
- **Українською**: Метод
- **Example**: `take_damage()` is a method on the `Player` class that reduces the player's health attribute by a given amount.

### Self
- **English**: The first parameter of every instance method in Python. It refers to the current object itself, letting the method access its own attributes and methods.
- **Українською**: Self (поточний об'єкт)
- **Example**: In `def heal(self, amount):`, `self.health` refers to the health of the specific player who is being healed.

### Module
- **English**: A single `.py` file in Python that can be imported by other files. It groups related functions, classes, and variables.
- **Українською**: Модуль
- **Example**: `game/player.py` is a module that contains only the `Player` class and its logic.

### Package
- **English**: A folder containing one or more modules together with an `__init__.py` file. Packages let you organize modules into a directory tree.
- **Українською**: Пакет
- **Example**: The `game/` folder is a package that bundles the `player`, `location`, `game`, and `data` modules.

### Route
- **English**: A mapping in Flask between a URL path (like `/game`) and a Python function that decides what the server should return.
- **Українською**: Маршрут
- **Example**: `@app.route("/game", methods=["GET"])` defines the route that renders the main gameplay screen.

### Endpoint
- **English**: A specific URL path plus HTTP method that the server responds to. Often used interchangeably with route, though endpoint emphasizes the external address.
- **Українською**: Ендпоінт
- **Example**: The `/action` endpoint accepts POST requests with an action ID and updates the game state in the session.

### Request
- **English**: The data Flask receives from the browser when a user visits a URL or submits a form. It includes form fields, cookies, headers, and more.
- **Українською**: Запит
- **Example**: When the user clicks "Go to Forest", `request.form.get("action")` reads the action ID from the POST request.

### Response
- **English**: The data Flask sends back to the browser — typically an HTML page, a redirect, or JSON. It is the result of calling a route function.
- **Українською**: Відповідь
- **Example**: After processing an action, Flask returns a response that redirects the player back to the `/game` page.

### Redirect
- **English**: A response that tells the browser to automatically navigate to a different URL instead of showing content immediately.
- **Українською**: Перенаправлення
- **Example**: After submitting a name at `/start`, the code uses `redirect(url_for("game_view"))` to send the player to the game screen.

### Render
- **English**: The process of taking a template and dynamic data, combining them, and producing the final HTML that is sent to the browser.
- **Українською**: Рендеринг
- **Example**: `render_template("game.html", player=..., location=...)` fills the `game.html` template with the current player stats and location.

### Template
- **English**: An HTML file with placeholes that Jinja2 fills in with real data. Templates let you keep HTML layout separate from Python code.
- **Українською**: Шаблон
- **Example**: `templates/game.html` is a template that displays the player's HP bar and renders one button per available action.

### Jinja2
- **English**: The templating engine built into Flask. It uses `{{ variable }}` for output and `{% %}` for control flow like loops and conditionals inside templates.
- **Українською**: Jinja2
- **Example**: In `game.html`, `{% for action in actions %}` is a Jinja2 loop that creates a button for each available action.

### GET
- **English**: An HTTP method used to read data from the server. It should not change anything permanently. URLs you visit in the browser normally use GET.
- **Українською**: GET
- **Example**: The `/game` route uses `methods=["GET"]` because it only reads and displays the current game state without modifying it.

### POST
- **English**: An HTTP method used to send data to the server to cause a change, such as starting a game, submitting a form, or performing an action.
- **Українською**: POST
- **Example**: The `/action` route accepts POST requests because every player action permanently changes health, score, or inventory.

### Form
- **English**: An HTML element that collects user input and sends it to the server. This project uses POST forms exclusively for gameplay actions.
- **Українською**: Форма
- **Example**: Each action button in `game.html` lives inside its own `<form method="POST">` that posts to the `/action` endpoint.

### Session
- **English**: A per-user storage mechanism in Flask that persists data between page loads using a signed cookie. This project uses it to save game state.
- **Українською**: Сесія
- **Example**: After creating a `Game` object, the app stores it as a dict in `session["game_state"]` so it survives page refreshes.

### Inventory
- **English**: The list of items a player is carrying, such as potions, keys, swords, or maps. In this project it is stored as a Python list.
- **Українською**: Інвентар
- **Example**: When you buy a Healing Potion in the Shop, the `add_item("potion")` method appends it to the player's inventory list.

### Health
- **English**: A numeric value representing how much damage a player can take before losing. In this project it starts at 100 and 0 means Game Over.
- **Українською**: Здоров'я
- **Example**: Fighting the cave monster deals 35 damage, reducing the `health` attribute and potentially ending the run if it reaches zero.

### Score
- **English**: A numeric value that rewards exploration and combat. It is used as currency in the Village Shop to buy Healing Potions.
- **Українською**: Рахунок (бал)
- **Example**: Finding the Castle Key awards +30 score, and each Healing Potion in the Shop costs 10 score to buy.

### Location
- **English**: A named place in the game world with its own description and available actions — Village, Forest, Cave, Shop, or Ancient Castle.
- **Українською**: Локація
- **Example**: The Forest is a location whose actions include searching the woods, returning to the Village, or entering the Cave.

### Action
- **English**: A button the player can click from their current location. Each action triggers a method on the Game class and mutates the state.
- **Українською**: Дія
- **Example**: "Explore the cave carefully" is an action in the Cave that, once per run, grants the Castle Key and +30 score.

### pytest
- **English**: The most popular Python testing framework. It discovers files named `test_*.py`, runs functions starting with `test_`, and reports pass/fail.
- **Українською**: pytest
- **Example**: Running `pytest -v` executes `tests/test_player.py` and `tests/test_game.py` to verify player healing and key-giveout logic.
