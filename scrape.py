#!/usr/bin/python3

from gmusicapi import Mobileclient
from dotenv import load_dotenv

load_dotenv()

def save_top_songs():
    with open('playlists/Thumbs up', 'w') as output:
        for song in api.get_top_songs():
            output.write("{} - {}\n".format(song['artist'], song['title']))


def save_user_playlists():
    playlists = api.get_all_user_playlist_contents()
    for p in playlists:
        name = p['name']
        with open('playlists/{}'.format(name), 'w') as file:
            for t in p['tracks']:
                file.write("{} - {}\n".format(t['track']['artist'], t['track']['title']))


api = Mobileclient()
# api.perform_oauth()

api.oauth_login(os.getenv('GMUSIC_OAUTH'))

save_user_playlists()
save_top_songs()
