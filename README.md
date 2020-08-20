A Python script to migrate your Google Play Music playlists to Spotify!

# Setup
You need to register application with Spotify to access their api. 
You can do this [here](https://developer.spotify.com/dashboard/applications).

Next you will want to setup your `.env` file with the info from the Spotify Dashboard.
You can do this by modifying the `.env.example` and renaming it to `.env`.

Then, assuming you have `python3` installed run `pip3 install -r requirements.txt`.

# Run
First you will need to scrape your playlists from G Music by running `python3 scrape.py`

