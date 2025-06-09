# SteamArchiver
A fast and lightweight command-line tool to quickly export your Steam game manifests and keys.

[English](README.md) | [简体中文](README_zh.md)

# 📖 About

SteamArchiver is a simple yet powerful utility for Steam users. It provides a quick, one-click way to export your game manifest and keys directly. It's designed to be minimal, fast, and easy to use, making it perfect for archiving your library or sharing a list of your games with friends.

# ✨ Features

⚡ Fast & Lightweight: No heavy dependencies, ensuring quick execution.

🔑 Key Export: Easily fetches and export your game manifests and keys.

🔒 Secure: Your credentials are only used to communicate with SteamDB, and it will never break any data on your devices

⚙️ Simple Setup: Get up and running with just a few commands.

# 🚀 Getting Started

Follow these instructions to get the project set up and running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

1. Ensure that your operating system is **Windows**.
2. Python 3.12 or higher installed.
3. uv: A fast Python package installer and resolver. You can install it via pip:

```bash
pip install uv
```
## Installation & Usage

1. Clone the repository

```bash
git clone https://github.com/Kaguya233qwq/SteamArchiver.git
cd SteamArchiver
```

2. Sync Dependencies

```bash
uv sync
```

3. First Run (Configuration)

Run the application for the first time to generate the configuration file.

```bash
uv run python main.py
```

The program will detect that this is the first run and create a .env file in the project directory. You now need to populate this file with your authentication details.
How to get your User-Agent and Cookie:

a. Open your web browser and navigate to steamdb.info/sub/. Make sure you are logged in.

b. Open your browser's Developer Tools (usually by pressing F12 or Ctrl+Shift+I).

c. Go to the Network tab.

d. Refresh the page (press F5).

e. Find and click on a request made to steamdb.info in the list of network requests.

f. In the Headers section (sometimes called "Request Headers"), find and copy the entire string values for User-Agent and Cookie.

Now, open the .env file and paste the values in, like so:

```
USER_AGENT=Your User-Agent string here
COOKIE=Your complete cookie string here
```

4. Export Your Game manifests and keys

With the .env file configured, run the program again.

```bash
uv run python main.py
```

The program will now prompt you to enter the app_id of the game you wish to export details for. After you provide the ID, it will fetch and output a fold with data.

# 📄 Disclaimer

## Important Notice

- This project does not provide any means or data to modify original game files or data in any way.
- Its sole purpose is to provide a convenient way for players to archive and share their personal game manifests.
- SteamArchiver is completely open-source and free to use. All commercial use is discouraged.

# 🤝 Contributing

Contributions are welcome! If you have suggestions or want to improve the tool, please feel free to open an issue or submit a pull request.

# 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.
