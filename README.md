<img align="right" src="https://cdn.discordapp.com/attachments/865173636364369921/980886211143028817/Artboard_1.svg" width=200px/>
<div align="center">
  <h1>Discerpo</h1>
  <p>A discord bot which helps with binary exploitation</p>
</div>

## Features
- Displaying dissasembled contents of a file (currently only PE files are "supported", support planed for ELF and possibly Mach-O)
- Accept files as URL and attachement
- Usage via slash commands and old-style commands

## Todo list
- Display imports, exports and such
- Add support for ELF and Mach-O
- Add timing and sync commands
- Display Entropy and generate an image based off of it
- ~~Potentially accept attachements not only URL~~ (Done)

## Installation
- Clone the repository ```git clone https://github.com/f1ammable/discerpo.git```
- Install poetry (if not installed already) https://python-poetry.org/
- Initialise venv by running ```poetry shell``` inside the cloned folder
- Install dependencies with ```poetry install```
- Create a new file called `botToken.py` in the root folder and use this template ```token = "YourTokenGoesHere"```
- run using ```python bot.py``` or ```python3 bot.py``` if you happen to be running on osx/linux

## Commands
- `disasm {architecture} {mode} {attachement}` (slash command: Slash command only as it's easier to handle attachements this way) - Sends content of disassembled binary
- `disasm_url {architecture} {mode} {file url}` (hybrid command: just so it's easier to use) - Works the same as the above command except it takes a file url instead of an attachement
-  ```rm_file``` (hybrid command) - deletes all files that have been generated by the user. This is done automatically when the user requests a new file to be disassembled, but it is a nice option regardless.
-  ```timer {command}``` (WIP: hybrid command) - Command to measure the performance of any command available
-  ```commandSync {guild}``` (WIP: hybrid command) - Command to sync the command tree of the bot per guild or globally. 
-  ```help``` (WIP: hybrid command) - displays all available commands
