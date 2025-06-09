from datetime import datetime
import json
import os
import shutil
from pathlib import Path
from typing import List
import urllib.request

from bs4 import BeautifulSoup


def _exit_after_seconds(seconds: int = 5):
    """Exits the program after a specified number of seconds"""
    import time

    print(f"Program will be exiting in {seconds} seconds...")
    time.sleep(seconds)
    # Force to exit the program, it means some configure has not set correctly
    exit(0)


def _get_data_from_steamdb(app_id: str) -> dict:
    """Fetches the game data on SteamDB"""
    url = f"https://steamdb.info/app/{app_id}/depots/"

    depot_ids = []
    user_agent = os.getenv("User-Agent")
    cookie = os.getenv("Cookie")
    headers = {
        # "User-Agent" and "Cookie" can be found in your browser with push the key "f12"
        # and they must be matched
        "User-Agent": user_agent,
        "Cookie": cookie,  # When the cookie expired (403 http error), just change it
        "Referer": url,
        # You will get a 451 error code if the 'Accept' not set
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        print(f"Fetching data for App ID: {app_id} ...")
        with urllib.request.urlopen(request) as resp:
            content = resp.read().decode("utf-8")
            soup = BeautifulSoup(content, "lxml")
            h1_tag = soup.find("h1", attrs={"itemprop": "name"})
            title = h1_tag.get_text(strip=True) if h1_tag else "Unknown Game"
            print(f"Game Title: {title}")
            table = soup.find("div", attrs={"id": "depots"})
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            for row in rows:
                if "data-depotid" in row.attrs:
                    depot_id = row["data-depotid"]
                    depot_ids.append(depot_id)
            print(f"Found {len(depot_ids)} depot IDs for App ID {app_id}.")
            return {
                "app_id": app_id,
                "title": title,
                "depot_ids": depot_ids,
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise GameNotFoundError(f"Game with App ID {app_id} not found on SteamDB.")
        elif e.code == 403:
            raise ForbiddenRequestError(
                "Access to the requested resource is forbidden."
            )
        else:
            raise SteamArchiverError(f"HTTP error occurred: {e}")


def env_parser() -> None:
    """Parses the .env file for User-Agent and Cookie"""
    from dotenv import load_dotenv

    env = Path(".env")
    if not env.exists():
        env.touch()
        with open(env, "w") as f:
            f.write(f"User-Agent=\n")
            f.write(f"Cookie=\n")
        print(f"Created .env file successfully at {env}")
        print(
            "Please fill in the User-Agent and Cookie values and restart the program."
        )
        _exit_after_seconds()
    else:
        load_dotenv(env)
        user_agent = os.getenv("User-Agent")
        cookie = os.getenv("Cookie")
        if not user_agent or not cookie:
            print("User-Agent or Cookie not set in .env file.")
            _exit_after_seconds()
        print("User-Agent and Cookie loaded successfully √")


def _get_steam_install_path() -> Path:
    """Returns the Steam installation path."""
    import platform

    if platform.system() == "Windows":
        import winreg

        key_path = "Software\\Valve\\Steam"
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                key_path,
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_32KEY,
            ) as key:
                # Query the InstallPath value
                value, _ = winreg.QueryValueEx(key, "InstallPath")
                if not value:
                    print("Steam not found. Please install Steam first.")
                    _exit_after_seconds()
                print(f"Steam installed in: `{Path(value)}` √")
                return Path(value)
        except FileNotFoundError:
            print("Steam not found in the registry. Please install Steam first.")
            _exit_after_seconds()
    elif platform.system() == "Linux":
        raise PlatformNotSupportedError("This program is not supported on Linux yet.")
    elif platform.system() == "Darwin":  # macOS
        raise PlatformNotSupportedError("This program is not supported on macOS yet.")
    else:
        raise PlatformNotSupportedError(
            "Unsupported operating system. What the hell are you using?"
        )


def _read_config_of_steam(steam_install_path: Path) -> dict:
    """Reads the Steam configuration file"""
    config_path = steam_install_path / "config" / "config.vdf"
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Parse the VDF content
    import vdf

    config_data = vdf.loads(content)
    return config_data


def _get_manifest_path_list(steam_install_path: Path, depot_ids: list) -> List[Path]:
    """Returns a list of manifest paths for the given depot IDs"""
    results = []
    depotcache = steam_install_path / "depotcache"
    manifest_files = [i for i in depotcache.glob("*.manifest")]
    for depot_id in depot_ids:
        for manifest_file in manifest_files:
            if manifest_file.name.startswith(f"{depot_id}_"):
                results.append(manifest_file.absolute())

    return results


def export(steam_install_path: str, app_id: str) -> None:
    """Exports the game data as a zip file"""
    if not Path("output").exists():
        Path("output").mkdir()
        
    data = _get_data_from_steamdb(app_id)
    depot_ids = data.get("depot_ids", [])

    time = datetime.now().strftime("%Y%m%d%H%M%S")
    app_path = Path("output") / f"archive_{app_id}_{time}"
    if not app_path.exists():
        app_path.mkdir()

    # compare the local depot which is installed
    local_depot_data = []
    config = _read_config_of_steam(steam_install_path)
    depots: dict = config["InstallConfigStore"]["Software"]["Valve"]["Steam"].get(
        "depots", {}
    )
    for depot_id, key in depots.items():
        if depot_id in depot_ids:
            local_depot_data.append(
                {
                    "depot_id": depot_id,
                    "key": key.get("DecryptionKey", ""),
                }
            )

    # ganerate a file to record the local depot data
    keys_txt = app_path / "keys"
    with open(keys_txt, "w", encoding="utf-8") as f:
        f.write(json.dumps(local_depot_data, indent=4))

    # Get the manifest paths for the local depots
    manifest_paths = _get_manifest_path_list(
        steam_install_path, [depot["depot_id"] for depot in local_depot_data]
    )

    # copy the manifest files to the output directory
    for manifest_path in manifest_paths:
        shutil.copy(manifest_path, app_path / manifest_path.name)

    # make a md5 file for verification
    md5_file = app_path / "security.md5"
    with open(md5_file, "w", encoding="utf-8") as f:
        for manifest_path in app_path.glob("*"):
            md5_hash = _calculate_md5(manifest_path)
            if md5_hash:
                f.write(f"{manifest_path.name} {md5_hash}\n")

    # archive the app directory
    _make_zip(app_path)

    print(f"Exported data for App ID {app_id} to {app_path.absolute()} successfully.")


def _calculate_md5(file_path, chunk_size=8192):
    import hashlib

    """Calculates the MD5 hash of a file in chunks to handle large files."""
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:  # read the file in binary mode
            while chunk := f.read(chunk_size):
                md5_hash.update(chunk)
    except IOError:
        print(f"Error: failed to read the file {file_path}")
        return None
    return md5_hash.hexdigest()


def _make_zip(path: Path) -> None:
    """Creates a zip file from the given path"""
    import zipfile

    zip_path = path.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in path.rglob("*"):
            if file.is_file():
                zipf.write(file, file.relative_to(path))


def print_banner() -> None:
    """Prints the banner: Steam Archiver"""
    banner = r"""
 ____  _                          _             _     _                
/ ___|| |_ ___  __ _ _ __ ___    / \   _ __ ___| |__ (_)_   _____ _ __ 
\___ \| __/ _ \/ _` | '_ ` _ \  / _ \ | '__/ __| '_ \| \ \ / / _ \ '__|
 ___) | ||  __/ (_| | | | | | |/ ___ \| | | (__| | | | |\ V /  __/ |   
|____/ \__\___|\__,_|_| |_| |_/_/   \_\_|  \___|_| |_|_| \_/ \___|_|   
   
                [+] A fast and lightweight tool for your Steam keys
                [+] https://github.com/Kaguya233qwq/SteamArchiver
"""
    print("\033[94m"+banner+"\033[0m")


class SteamArchiverError(Exception):
    """Custom exception for Steam Archiver errors"""


class GameNotFoundError(SteamArchiverError):
    """Exception raised when a game is not found on SteamDB"""


class ForbiddenRequestError(SteamArchiverError):
    """Exception raised when a request is forbidden"""


class PlatformNotSupportedError(SteamArchiverError):
    """Exception raised when the platform is not supported"""


if __name__ == "__main__":
    try:
        print_banner()
        env_parser()
        steam_install_path = _get_steam_install_path()
        app_id = input("Enter the App ID of the game: ").strip()
        export(steam_install_path, app_id)
    except SteamArchiverError as e:
        print(f"Error: {e}")
        _exit_after_seconds()
