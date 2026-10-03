# Python Adventure Lab: Setup, Run, and Build Guide

This guide takes you from a downloaded copy of the project to a working game in your browser. It covers Windows, macOS, and Linux.

## What "build" means for this project

Python Adventure Lab is a Flask web application. There is no separate compile step and no installer or `.exe` to build. You download the source code, create an isolated Python environment, install the required packages, and run the local web server. The first package installation needs an internet connection; playing the game afterward does not use external services.

## Requirements

- Python 3.11 or newer.
- A web browser.
- Internet access for the first installation of Python packages.
- A terminal: PowerShell on Windows, or Terminal on macOS/Linux.

You do not need Git if you download the project as a ZIP file. You do not need to install Flask globally.

## 1. Download and open the project

1. Download the project as a ZIP file, or get a copy from your teacher.
2. Extract the ZIP file. Do not run commands from inside the ZIP preview.
3. In VS Code, choose **File > Open Folder** and open the project folder. It is the folder that contains `requirements.txt`, `app.py`, and the `game`, `templates`, and `static` folders.
4. Open a terminal in VS Code with **Terminal > New Terminal**. The terminal should start in the project folder. Check with:

   ```text
   dir
   ```

   On macOS/Linux, use `ls`. Make sure `requirements.txt` appears in the listing. If it does not, open the inner project folder extracted from the ZIP.

## 2. Check Python

In the terminal, check that Python is installed:

**Windows (PowerShell):**

```powershell
python --version
```

If that command is not recognized, try the Python launcher:

```powershell
py -3 --version
```

**macOS/Linux:**

```bash
python3 --version
```

The version must be 3.11 or newer. If Python is missing on Windows, install it from [python.org](https://www.python.org/downloads/) and select **Add python.exe to PATH** in the installer. Then close and reopen VS Code and check the version again. If `python` opens the Microsoft Store, turn off the `python.exe` and `python3.exe` app execution aliases in Windows Settings, or use `py -3` if it works.

## 3. Create an isolated environment and install packages

Run these commands from the project folder. They use the Python inside `.venv` directly, so activating the environment is not required.

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

If `python` is unavailable but `py -3 --version` worked, use this command instead to create the environment:

```powershell
py -3 -m venv .venv
```

Then install the packages:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The install can take a minute. Flask, pytest, and python-dotenv are installed into this project environment, not into your system Python. The `.venv` folder is local to your computer and should not be submitted or included in a project ZIP.

## 4. Start the game

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\python.exe app.py
```

**macOS/Linux:**

```bash
.venv/bin/python app.py
```

Wait until the terminal shows a line similar to:

```text
Running on http://127.0.0.1:5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Keep the terminal open while you play. To stop the server, focus the terminal and press **Ctrl+C**.

This is a local development server. It is intended for your own computer, not for publishing the game to the internet. The app starts in debug mode by default; do not expose it to a public network.

## 5. Run the tests (optional)

Stop the server with **Ctrl+C**, or open a second terminal in the project folder.

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

**macOS/Linux:**

```bash
.venv/bin/python -m pytest -v
```

Pytest should report the test results in the terminal. You can start the game again with the command in step 4.

## Troubleshooting

### `python` was not found, or Windows suggests the Microsoft Store

Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/), select **Add python.exe to PATH**, and restart VS Code. If the `py -3 --version` command works, use `py -3 -m venv .venv` in step 3. If the Microsoft Store still opens, disable the Python app execution aliases in Windows Settings.

### `No module named 'flask'` or `No module named 'dotenv'`

Install packages using the `.venv` Python command in step 3. Confirm that the terminal is in the folder containing `requirements.txt`. Do not use a different system-wide `pip` command.

### `.venv` or its Python executable cannot be found

Run the environment-creation command in step 3 from the project folder. On Windows, check that `.venv\Scripts\python.exe` exists; on macOS/Linux, check that `.venv/bin/python` exists.

### PowerShell says scripts are disabled

No activation script is needed for this guide. Run the commands using `.\.venv\Scripts\python.exe` as shown above; this avoids changing PowerShell's execution policy.

### The browser cannot connect, or port 5000 is already in use

Keep the terminal running and use the exact address `http://127.0.0.1:5000`. If another copy of the app is already using port 5000, stop that copy with **Ctrl+C** in its terminal, then start the app again.

### Package installation fails

Check your internet connection and repeat the install command from step 3. If your school network blocks package downloads, ask your teacher or network administrator for help.

## Quick checklist

- The terminal is open in the folder containing `requirements.txt`.
- Python 3.11 or newer is available.
- The `.venv` environment was created and the package installation completed without errors.
- The server terminal shows `Running on http://127.0.0.1:5000`.
- The game opens at `http://127.0.0.1:5000`.