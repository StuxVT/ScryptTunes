## Need to rewrite instructions to be more comprehensive, if you need help, contact me. Happy to help set up:
- Discord: @stuxvt
- Twitter: @stuxvt

# ScryptTunes

Welcome to ScryptTunes! This application allows you to control your Spotify playlist through Twitch chat commands. This guide will walk you through the installation and setup process, step-by-step.

NOTE: This bot requires Spotify Premium. This is a Spotify API reqirement and there's nothing I can do about it

### Dev Announcements:
 - Channel points redeem is broken, working on a fix. I will disable it in the next release. Don't use it, just doesnt work at all!

## Table of Contents
1. [Install](#install)
2. [Setup](#setup)
3. [Usage](#usage)

 ## Install
1. Go to the latest release page here: [ScrypTunes Latest Release](https://github.com/StuxVT/ScryptTunes/releases/latest)
2. Download `ScryptTunesInstaller.exe` and run it
3. ScryptTunes will now show up in your start menu and as a desktop shortcut

## Setup
### 1. General
1. Open ScryptTunes and click the "Settings" button.
2. Fill in the following fields:
    - **Nickname**: Name of bot account.
      - If you don't use a separate twitch account for your bot, just put your channel name here.
    - **(Optional) Prefix**: Enter the command indicator for Twitch chat (e.g., `!`). 
    - **Channel**: Channel to listen for commands from. (Very likely to be your twitch channel name)
    - **Token**: Get your Twitch OAuth token from [Twitch Token Generator](https://twitchtokengenerator.com/) and select "Bot Chat Token"
        - Make sure you sign in with the account you want sending bot messages into your chat
  
 ![image](https://github.com/user-attachments/assets/9f06212e-30ed-4c20-9c18-9b2851478889)



### 2. Setting Up Spotify
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Click "Create an App" and fill in the necessary details.
 a. The only important one to get is to fill the "redirect uri" as `http://localhost:8080` WITHOUT A SLASH AT THE END 

3. Once the app is created, click settings.

4. You'll see a "Client ID" and "Client Secret". Enter these in the Settings view of ScryptTunes.

![image](https://github.com/user-attachments/assets/7a6456b1-9469-43d5-92e9-9b564998cfd3)


### 3. Setting Up Twitch
1. Visit the [Twitch Developer Console](https://dev.twitch.tv/console).
2. Click "Applications" >> "Register Your Application" and fill in the necessary details.
3. Click on "Manage" for your app
4. You'll see a "Client ID" and "Client Secret". Enter these in the Settings view as well.

![image](https://github.com/user-attachments/assets/57b52867-ae39-412d-b1d4-059d38dfbf66)


### 4. App Settings
### ${\color{red}BE \space SURE \space TO \space CLICK \space SAVE}$

## Usage
1. Start playing music on Spotify
2. Click "Start" on the main page to start the bot
3. If you need help with commands see the [Commands Guide](https://github.com/StuxVT/ScryptTunes/wiki/Commands#scrypttunes-commands-guide)

---

## Credits
### `🎶` [TwitchTunes](https://github.com/mmattDonk/TwitchTunes)
- Originally forked from this project, has grown to have many more features, fixes, etc, but [mattDonk](https://github.com/mmattDonk) deserves credit for the starting point.

---
## Dev Notes
You can just run main.py, or build locally if necessary. Feel free to ask questions in DMs on my
[Twitter](https://twitter.com/stuxvt) or [Discord](http://discord.stux.ai) but please google first.
### Build Locally
`python -m nuitka --standalone --enable-plugin=tk-inter --include-data-file=icon.ico=icon.ico --output-dir="build" --output-filename="ScryptTunes.exe" .\main.py`
### Create Installer
`makensis installer.nsi`
