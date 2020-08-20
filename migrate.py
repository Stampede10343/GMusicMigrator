#!/usr/bin/python3
import spotipy
from spotipy import SpotifyOAuth
import glob
import os
import sys
import logging

logging.basicConfig("output.log", level=logging.DEBUG)
LOG = logging.getLogger()

def has_artist(artist, artists):
    cleaned = list(map(lambda art: art['name'], artists))
    a = list(filter(lambda a: artist == a, cleaned))
    return artist in a

def save_track(saved_tracks, track):
    saved_tracks.append(track)

def pick_track(saved_tracks, tracks):
    sorted_tracks = list(sorted(tracks, key=lambda track: track['popularity']))
    for i, track in enumerate(sorted_tracks):
        print("Please select a track:")
        print("{})".format(i), track['name'], track['artists'][0]['name'])

    while True:
        selection = input("Select a track (or -1 to skip):")
        if select == -1:
            break
        elif select >= 0 and select < len(sorted_tracks):
            save_track(saved_tracks, sorted_tracks[selection])
            break

def add_tracks_to_playlist(saved_tracks, playlist):
    LOG.log("Adding {} songs to playlist: {}", len(saved_tracks), playlist)

from dotenv import load_dotenv
load_dotenv()

scope = "playlist-modify-private"
auth = SpotifyOAuth(scope=scope,
                    username=os.getenv("SPOTIFY_USERNAME"),
                    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                    redirect_uri="http://localhost")
LOG.debug("Running with token: {}", auth.get_access_token())

sp = spotipy.Spotify(auth_manager=auth)

for playlist in glob.glob('playlists/*'):
    saved_tracks = []
    with open(playlist, 'r') as file:
        for line in file:
            artist_song = line.replace('\n', '').split(' - ')
            artist = artist_song[0]
            song = artist_song[1]

            result = sp.search(artist + ' ' + song)
            tracks = result['tracks']['items']
            if len(tracks) == 0:
                LOG.log("Track not found: {} - {}".format(artist, song))
            elif len(tracks) == 1:
                LOG.debug("Ideal case")
            else:
                exact_matches = list(filter(lambda t: song in t['name'] and
                                            has_artist(artist, t['artists']), tracks))
                if len(exact_matches) == 0:
                    LOG.debug("No exact matchs")
                    pick_tracks(saved_tracks, tracks)
                elif len(exact_matches) == 1:
                    LOG.debug('One exact matching result')
                    save_track(saved_tracks, exact_matches[0])
                else:
                    pick_track(saved_tracks, exact_matches)
            print()
            break

        add_tracks_to_playlist(saved_tracks, playlist)
    pass

