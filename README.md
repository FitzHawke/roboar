# Reboar

<div align="center">
  <img src="./assets/wild-boar-head.svg" alt="Logo" width="240" height="240">
</div>

⚠ **Effectively unmaintained and poorly documented, but still works as far as I know**

Old un-optimized python script that is extremely tuned to my specific use-case; copying, re-tagging and/or re-encoding music so it would sort properly and play on my cars soundsystem. Converting FLAC to .ogg as that is the best codec the stereo supports.

- UI is just a basic CLI input of a comma-separated list to indicate the actions you want to take.
- select artists then cycle through selecting individual albums, for delete, modify, and add. Does not take any actions until all selections are made.
- uses information from path to generate tags
- expects directory structure of the form `/<music_root>/<artist_name>/[<year>] - <album_name>/<album_number>-<track_number> - <track_name>` but also accepts `/<music_root>/<artist_name>/[<year>] - <album_name>/<track_number> - <track_name>`
- converts multi-album to single album for improved sorting
- fun fact, v1.0 (which heroically sacrificed itself to teach me the value of backups) was one of my earliest programming projects. It was a gloriously unreadable mess of poorly named functions/classes/variables based on a nautical pirate theme combined with amateur attempts at handling unicode/ascii in python2 😱. But, in spite of that, it also had a dedicated config file, options of outputs, checking files for updated versions, and probably more features I've forgot. And the peculiar thing is this, my friends, the code we wrote on that fateful night, it didn't actually look anything like this code. So you see, this is not the greatest reboar in the world, no, this is just a [tribute](https://www.youtube.com/watch?v=_lK4cX5xGiQ).

Might someday update to be more robust/support other formats, but in the age of spotify my music collection is stagnant so this doesn't receive much attention. Reach out to me if that seems like it'd be useful to you.

Requires mutagen and ffmpeg to work. Settings are variables set at the top of init.py
