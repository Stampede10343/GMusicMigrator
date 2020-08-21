#!/usr/bin/python3
import spotipy
from spotipy import SpotifyOAuth
import glob
import os
import sys
import logging

logging.basicConfig(filename="output.log", level=logging.DEBUG)
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

def has_artist(artist, artists):
    cleaned = list(map(lambda art: art['name'], artists))
    a = list(filter(lambda a: artist == a, cleaned))
    return artist in a

def save_track(saved_tracks, track):
    saved_tracks.append(track)

def pick_track(saved_tracks, tracks):
    sorted_tracks = list(sorted(tracks, key=lambda track: track['popularity'], reverse=True))
    print("Please select a track:")
    for i, track in enumerate(sorted_tracks):
        print("{}) {} - {} - {}".format(i, track['name'], list(map(lambda t: t['name'], track['artists'])), track['album']['name']))

    while True:
        selection = input("Select a track (or -1 to skip): ")
        try:
            selection = int(selection)
            if selection == -1:
                break
            elif selection >= 0 and selection < len(sorted_tracks):
                save_track(saved_tracks, sorted_tracks[selection])
                break
        except Exception as e:
            pass

def add_tracks_to_playlist(saved_tracks, playlist):
    LOG.info("Adding %s songs to playlist: %s", len(saved_tracks), playlist)
    track_ids = list(map(lambda t: t['id'], saved_tracks))
    user_id = sp.current_user()['id']
    user_playlists = sp.user_playlists(user_id)['items']

    if len(user_playlists) == 0:
        created_playlist = sp.user_playlist_create(user_id, playlist)
        playlist_id = created_playlist['id']
        print(playlist_id)
        sp.user_playlist_replace_tracks(user_id, playlist_id, track_ids)
        pass
    else:
        print(user_playlists)
        existing_playlists = list(filter(lambda p: playlist == p['name'], user_playlists))
        if len(existing_playlists) == 0:
            created_playlist = sp.user_playlist_create(user_id, playlist)
            playlist_id = created_playlist['id']
            sp.user_playlist_replace_tracks(user_id, playlist_id, track_ids)
        elif len(existing_playlists) == 1:
            sp.user_playlist_replace_tracks(user_id, existing_playlists[0]['id'], track_ids)
        else:
            LOG.err("Multiple playsts with name exists?? %s", existing_playlists)


def find_song(line, saved_tracks):
    artist_song = line.replace('\n', '').split(' - ')
    artist = artist_song[0]
    song = artist_song[1]

    result = sp.search(artist + ' ' + song)
    tracks = result['tracks']['items']
    if len(tracks) == 0:
        LOG.warning("Track not found: %s - %s", artist, song)
    elif len(tracks) == 1:
        LOG.debug("Ideal case")
        save_track(saved_tracks, tracks[0])
    else:
        exact_matches = list(filter(lambda t: song in t['name'] and
                                    has_artist(artist, t['artists']), tracks))
        if len(exact_matches) == 0:
            LOG.debug("No exact matches")
            pick_track(saved_tracks, tracks)
        elif len(exact_matches) == 1:
            LOG.debug('One exact matching result')
            save_track(saved_tracks, exact_matches[0])
        else:
            pick_track(saved_tracks, exact_matches)

from dotenv import load_dotenv
load_dotenv()

scope = "playlist-modify-public"
auth = SpotifyOAuth(scope=scope,
                    username=os.getenv("SPOTIFY_USERNAME"),
                    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                    redirect_uri="http://localhost")
LOG.debug("Running with token: %s", auth.get_access_token())

sp = spotipy.Spotify(auth_manager=auth)

for playlist in glob.glob('playlists/*'):
    saved_tracks = []
    with open(playlist, 'r') as file:
        for line in file:
            find_song(line, saved_tracks)
            print()

        add_tracks_to_playlist(saved_tracks, playlist.split('/')[1])
    break

