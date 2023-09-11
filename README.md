# lmao what's a readme (improving this right away dont worry)

- Okay fine ill do a basic step by step for now:
    - Nickname
      - Name this the same as the bot/account name who the twitch oauth belongs to
    - Prefix
      - the command indicator in twitch chat.. ex: `!sr Never Gonna Give You Up - Rick Astley`
    - Channels
      - A list of channels for the bot to watch for commands
      - Definitely at least add your own channel in here
    - token
      - get a twitch OAuth token from here: [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/)
    - client_id and client_secret
      - You need to create your own twitch developer application
      - twitch developer application keys from here: [Create a Twitch Extension!](https://dev.twitch.tv/console/extensions/create)
    - channel_points_reward (optional)
      - EXACT name of your channel points reward -- i dont recommend using this, untested
    - spotify_client_id and spotify_secret
      - You need to create your own spotify developer application
      - https://developer.spotify.com/dashboard
  - spotify_redirect_url
    - you may change this, but make sure it matches the configuration in your spotify developer app


## Credits
- Song request queue for stream. Customized version of [TwitchTunes](https://github.com/mmattDonk/TwitchTunes) with various bugfixes and extra features (Like support for youtube links). All credit goes to [mattDonk](https://github.com/mmattDonk) for the majority of the baseline bot.
