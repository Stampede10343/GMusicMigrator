A Python script to migrate your Google Play Music playlists to Spotify!

# Setup
You need to register application with Spotify to access their api. 
You can do this [here](https://developer.spotify.com/dashboard/applications).

Next you will want to setup your `.env` file with the info from the Spotify Dashboard.
You can do this by modifying the `.env.example` and renaming it to `.env`.

Then, assuming you have `python3` installed run `pip3 install -r requirements.txt`.

# Run
First you will need to scrape your playlists from G Music by running `python3 g-auth.py`
This will give you a link to visit to grant API access after you enter the auth key returned.

After you've authenticated with G Music, you can then run the `scrape.py` script to pull your playlists
into the folder `playlist`.

## Migrate to Spotify
Once the playlists are ready in the folder `playlists`, you can now start the migration process.

**NOTICE** this script can be _destructive_ to existing playlists with the same names as the playlists from G Music.

If you have playlists with the same names already in Spotify, you can rename the playlists under `playlists/` 
to be unique in order help prevent removing songs from existing playlists.

After you have set up your `.env` file with your Spotify API information you can then run `python3 migrate.py`.
This should start song by song querying the Spotify API and prompting you to choose a version of the song when the
choice is not obvious.

Once all of the songs have been chosen the script will attempt to create the playlist if it doesn't exist, and
overwrite the playlist if it does exist.

If there were any songs that were not found in the search, you can check `output.log` for `warning`'s that will mention
which songs were not found and will have to be manually added to the playlist.

Currently I have the script only running one playlist at a time in case there are any issues, you will _have_
to remove or move the playlist that you just migrated from the `playlists` folder in order to migrate the next playlist.

# Feedback and Issues
This script _will_ have issues. I haven't done thorough testing of all scenarios, just enough to get my playlists moved over.
If you do run into an issue, please open a Github issue and if possible attach your `output.log` file.

