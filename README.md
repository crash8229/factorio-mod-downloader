# factorio-mod-downloader
A simple script to download Factorio mods listed in the mod-list.json that Factorio generates

## Dependencies

- Python 3
- Python Packages
  - requests
  - alive-progress

## Usage

The user-data.json file needs to be filled out with a valid Factorio account username and token. The token can be found on the profile page: https://factorio.com/profile

The script requires a single argument: the path to the mod-list.json \
By default, only mods that are enabled in the mod-list.json are downloaded. The flag `-a` can be passed to download all the mods regardless if they are enabled or not.

Example: `./factorio-mod-downloader.py mod-list.json`

Passing `-h` to the script shows a usage message.

``` text
usage: factorio_mod_downloader.py [-h] [-a] file

Factorio mod downloader. Downloads the enabled mods listed in the given mod-list.json. The mods are saved to a folder called `mods` in the current directory. The user-data.json file needs to be filled out with a
valid Factorio account username and token. The token can be found on the profile page: https://factorio.com/profile

positional arguments:
  file        Path to the mod-list.json

optional arguments:
  -h, --help  show this help message and exit
  -a, --all   Download all mods in the given mod-list.json
```
