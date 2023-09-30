# ScryptTunes

Welcome to ScryptTunes! This application allows you to control your Spotify playlist through Twitch chat commands. This guide will walk you through the installation and setup process, step-by-step.

## Table of Contents
1. [Install](#install)
2. [Setup](#setup)
3. [Setting Up Spotify](#setting-up-spotify)
4. [Setting Up Twitch](#setting-up-twitch)

## Install
1. Go to the latest release page here: [ScrypTunes Latest Release](https://github.com/StuxVT/ScryptTunes/releases/latest)
2. Download `ScryptTunesInstaller.exe` and run it
3. ScryptTunes will now show up in your start menu and as a desktop shortcut

## Setup
### General
1. Open ScryptTunes and click the "Settings" button.
2. Fill in the following fields:
    - **Nickname**: Enter the name of the bot/account to which the Twitch OAuth token belongs.
    - **(Optional) Prefix**: Enter the command indicator for Twitch chat (e.g., `!`).
    - **Channels**: Enter a list of Twitch channels where the bot should watch for commands. At least add your own channel.
    - **Token**: Get your Twitch OAuth token from [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/).

### Setting Up Spotify
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Click "Create an App" and fill in the necessary details.
3. Once the app is created, you'll see a "Client ID" and "Client Secret". Enter these in the Settings view.

### Setting Up Twitch
1. Visit the [Twitch Developer Console](https://dev.twitch.tv/console).
2. Click "Create an App" and fill in the necessary details.
3. Once the app is created, you'll see a "Client ID" and "Client Secret". Enter these in the Settings view as well.

## Usage
1. Start playing music on Spotify
2. Click "Start" on the main page to start the bot
3. If you need help with commands see the [Commands Guide](https://github.com/StuxVT/ScryptTunes/wiki/Commands#scrypttunes-commands-guide)

---

## Credits
### `🎶` [TwitchTunes](https://github.com/mmattDonk/TwitchTunes)
- I am using a customized version with various bugfixes and extra features (Like support for youtube links). 
   All credit goes to [mattDonk](https://github.com/mmattDonk) for the majority of the baseline bot.

---
## Dev Notes
### Build Locally
`python -m nuitka --standalone --enable-plugin=tk-inter --include-data-file=icon.ico=icon.ico 
--output-dir="build" --output-filename="ScryptTunes.exe" .\main.py`
### Create Installer
`makensis installer.nsi`
