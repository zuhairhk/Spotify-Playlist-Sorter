import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

f = open('items.txt', 'w')
# sys.stdout = f

def get_artist_genre(name):
    result = spotify.search(name)
    track = result['tracks']['items'][0]

    artist = spotify.artist(track["artists"][0]["external_urls"]["spotify"])
    print("artist genres:", artist["genres"], '\n')

def get_artist(track):
    for artist in track['track']['artists']:
        name = artist['name']
        print(name)
        get_artist_genre(name)

def get_tracks(pl_URI, tracks, count, offset):
    for track in spotify.playlist_tracks(pl_URI, offset=offset)['items']:
        try:
            track_uri = track['track']['uri']
            track_name = track['track']['name']
            result = track_name , spotify.audio_features(track_uri)
            tracks.append(result)
            print(track['track']['name'])
            get_artist(track)
            count += 1
            
        except (TypeError, AttributeError):
            print('None!?')

    return count

def run(target, count, offset):
    tracks = []

    if count <= target:
        count = get_tracks('4tsG3tuHtK3S3GoRCAl8n1', tracks, count, offset) # 26jDYsxAgRqpOIRovfWU9L
        offset += 100
        run(target, count, offset)
    else:
        print('------------------DONE------------------')

target = 32 # int(input('Enter total # of songs in playlist: '))
run(target=target, count=1, offset=0)
f.close()
# artist_genres = (spotify.artist(artist_id='0Y5tJX1MQlPlqiwlOH1tJY'))['genres']
# print(artist_genres)