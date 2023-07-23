#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from hashlib import sha1

import requests  # type: ignore
import alive_progress  # type: ignore

STD_LIBS = ["base"]


def main(json_file: Path, all: bool = False) -> None:
    with open(json_file, "r") as f:
        mod_list_raw = json.load(f)["mods"]
    with open("user-data.json", "r") as f:
        user_info = json.load(f)

    # Check user info
    if not user_info["user"] or not user_info["token"]:
        raise ValueError("Missing Factorio account information in user-data.json")

    status = requests.get(f'https://mods.factorio.com?username={user_info["user"]}&token={user_info["token"]}')

    # Process the mod list and extract only the ones we need
    mod_list = list()
    for mod in mod_list_raw:
        if not all and not mod["enabled"] or mod["name"] in STD_LIBS:
            continue
        mod_list.append(mod)

    # Ensure the folder to save the mods to exists
    out_folder = Path("mods")
    out_folder.mkdir(exist_ok=True)

    # Download the mods
    print(f"Downloading {len(mod_list)} mods")
    bar = alive_progress.alive_it(mod_list, finalize=lambda bar: bar.text('Done'))
    for mod in bar:
        bar.text(f'Downloading {mod["name"]}')
        status = requests.get(f'https://mods.factorio.com/api/mods/{mod["name"]}')
        if status.status_code != 200:
            print(f'Failed to get mod info: {mod["name"]}')
            continue
        mod_info = json.loads(status.text)
        latest_mod_version = mod_info["releases"][-1]
        out_file = out_folder.joinpath(latest_mod_version["file_name"])
        download_url = f'https://mods.factorio.com{latest_mod_version["download_url"]}?username={user_info["user"]}&token={user_info["token"]}'
        download_sha1 = latest_mod_version["sha1"]
        status = requests.get(download_url)
        if status.status_code == 403:
            print("Failed to authenticate: Check username and token")
            break
        elif status.status_code != 200:
            print(f'Failed to download mod: {mod["name"]}')
            continue
        content_sha1 = sha1(status.content).hexdigest()
        if content_sha1 != download_sha1:
            print(f'SHA1 check failed: {mod["name"]}: Calculated={content_sha1} Expected={download_sha1}')
            continue
        with open(out_file, "wb") as f:
            f.write(status.content)
        print(f'Downloaded {latest_mod_version["file_name"]}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Factorio mod downloader. Downloads the enabled mods listed in the given mod-list.json. The mods are saved to a folder called `mods` in the current directory. The user-data.json file needs to be filled out with a valid Factorio account username and token. The token can be found on the profile page: https://factorio.com/profile")
    parser.add_argument("file", help="Path to the mod-list.json", type=Path)
    parser.add_argument("-a", "--all", help="Download all mods in the given mod-list.json", action="store_true")
    args = parser.parse_args()
    main(args.file, args.all)
