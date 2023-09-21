# ScryptTunes: A Simple Guide for Windows Users

Welcome to ScryptTunes! This application allows you to control your Spotify playlist through Twitch chat commands. This guide will walk you through the installation and setup process, step-by-step.

## Table of Contents
1. [Installing Python](#installing-python)
2. [Downloading ScryptTunes](#downloading-scrypttunes)
3. [Running the UI](#running-the-ui)
4. [Entering Data in Settings](#entering-data-in-settings)
5. [Setting Up Spotify](#setting-up-spotify)
6. [Setting Up Twitch](#setting-up-twitch)

## Installing Python
1. Visit the [Python Downloads Page](https://www.python.org/downloads/windows/).
2. Download the latest version and run the installer.
3. Make sure to check the box that says "Add Python to PATH" during installation.

## Downloading ScryptTunes
1. Go to the [ScryptTunes GitHub repository](https://github.com/StuxVT/ScryptTunes).
2. Click on the green "Code" button and choose "Download ZIP".
3. Extract the ZIP file to a folder of your choice.

## Running the UI
1. Navigate to the folder where you extracted ScryptTunes.
2. Locate the `main.py` file and double-click on it to run the application.
    - The application will automatically install the required packages for you.

## Setup
1. Open ScryptTunes and go to the "Settings" view.
2. Fill in the following fields:
    - **Nickname**: Enter the name of the bot/account to which the Twitch OAuth token belongs.
    - **Prefix**: Enter the command indicator for Twitch chat (e.g., `!`).
    - **Channels**: Enter a list of Twitch channels where the bot should watch for commands. At least add your own channel.
    - **Token**: Get your Twitch OAuth token from [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/).

## Setting Up Spotify
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Click "Create an App" and fill in the necessary details.
3. Once the app is created, you'll see a "Client ID" and "Client Secret". Enter these in the Settings view.

## Setting Up Twitch
1. Visit the [Twitch Developer Console](https://dev.twitch.tv/console).
2. Click "Create an App" and fill in the necessary details.
3. Once the app is created, you'll see a "Client ID" and "Client Secret". Enter these in the Settings view as well.

## Usage
1. Start playing music on Spotify
2. Click "Start" on the main page to start the bot

---

## Credits
### `🎶` [TwitchTunes](https://github.com/mmattDonk/TwitchTunes)
- I am using a customized version with various bugfixes and extra features (Like support for youtube links). 
   All credit goes to [mattDonk](https://github.com/mmattDonk) for the majority of the baseline bot.
