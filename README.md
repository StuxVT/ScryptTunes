#### Song request queue for stream. Customized version of [TwitchTunes](https://github.com/mmattDonk/TwitchTunes) with various bugfixes and extra features (Like support for youtube links). All credit goes to [mattDonk](https://github.com/mmattDonk) for the majority of the baseline bot.

#### Also please dont look at my UI code i wrote this at like 4am oh god its so bad

## todo
- run with OBS start? maybe set this up with installer
- run as executable (terminal is hard for some)
- define some form of interface for custom input frames to standardize retrieving/setting values and other common tasks

## wish-list
(if i get time in the future)
- local browser source for queue visualization
- maybe implement the above into a twitch panel/plugin?
- bot code is "await" soup... make it actually async
- lots of "common code" possible inside bot, like permission checks
- prevent repeat-song spam
- dont spam logs with nonexistant commands
- flame certain users based on username (juzen, lum)


# todo for GUI
- create steb by step for setup
- validate blacklist files exist, other state validations?
  - fix error message on state invalid
- enable/disable buttons for start/stop bot respective to bot state (run event)
- settings need to be in scrollable frame
- set new size for settings view
- hide sensitive data in settings view/frame
- suppress/handle error when closing bot's asyncio loop
- clean up bot code (maybe try out the SonarLint plugin)
- create a useful readme like a good boy (challenge: impossible)

## stretch goal todos for today
- annotations(decorator)  for RBAC on bot commands?