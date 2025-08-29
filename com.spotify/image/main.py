import argparse
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import sys


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_playlist_items(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    while True:
        items = results['items']
        for item in items:
            yield item

        if not results['next']:
            break

        results = sp.next(results)


def auth(args):
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

    cache_handler = spotipy.MemoryCacheHandler()

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-read-private",
            cache_handler=cache_handler,
        )
    )

    user = sp.current_user()
    log(f"Authenticated as: {user['display_name']} ({user['id']})")
    print(json.dumps(cache_handler.token_info))


def playlist_tracks(args):
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    username = os.environ["SPOTIFY_USERNAME"]
    token_info = json.loads(os.environ["SPOTIFY_TOKEN_INFO"])

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-read-private",
            open_browser=False,
            cache_handler=spotipy.MemoryCacheHandler(token_info),
        )
    )
    user = sp.current_user()
    log(f"Authenticated as: {user['display_name']} ({user['id']})")

    playlists = sp.user_playlists(username)

    while playlists:
        for playlist in playlists['items']:
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            owner = playlist['owner']['display_name']
            
            log(f"Processing playlist: '{playlist_name}' of '{owner}'")

            for item in get_playlist_items(sp, playlist_id):
                item['playlist'] = playlist
                print(json.dumps(item))

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


if __name__ == '__main__':
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)
    
    # auth
    cmd = subparsers.add_parser('auth')
    
    # playlist-tracks
    cmd = subparsers.add_parser('playlist-tracks')

    args = parser.parse_args()
    log("Parsed args:", args)

    if args.cmd == 'auth':
        auth(args)
    elif args.cmd == 'playlist-tracks':
        playlist_tracks(args)
