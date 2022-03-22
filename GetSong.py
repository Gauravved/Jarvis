from dataclasses import replace
import spotipy as sp

class InvalidSearch(Exception):
    pass

def get_album_uri(spotify: sp, name: str) -> str:
    original = name
    name = name.replace(' ','+')
    results = spotify.search(q=name , limit=1, type='album')
    if not results['albums']['items']:
        raise InvalidSearch(f'No album found {original}')
    album_uri = results['albums']['items'][0]['uri']
    return album_uri

def play_album(spotify=None , device_id=None, uri=None):
    spotify.start_playback(device_id=device_id , context_uri=uri) 

def get_artist_uri(spotify: sp, name: str) -> str:
    original = name
    name = name.replace(' ','+')
    results = spotify.search(q=name , limit=1, type='artist')
    if not results['artists']['items']:
        raise InvalidSearch(f'No artists found {original}')
    artist_uri = results['artists']['items'][0]['uri']
    return artist_uri

def play_artist(spotify=None , device_id=None, uri=None):
    spotify.start_playback(device_id=device_id , context_uri=uri) 

def get_track_uri(spotify: sp, name: str) -> str:
    original = name
    name = name.replace(' ','+')
    results = spotify.search(q=name , limit=1, type='track')
    if not results['tracks']['items']:
        raise InvalidSearch(f'No track found {original}')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri

def play_track(spotify=None , device_id=None, uri=None):
    spotify.start_playback(device_id=device_id , uris=[uri]) 