import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

f = open('items.txt', 'w')
# sys.stdout = f

def get_artist_genre(name):
    try:
        result = spotify.search(name)
        track = result['tracks']['items'][0]
        artist = spotify.artist(track["artists"][0]["external_urls"]["spotify"])
        
        trackGenres.append(artist['genres'][0])

        for genre in artist['genres']:
            if genre not in genreList:
                genreList.append(genre)
                songDict[genre] = []

        return(artist['genres'])

    except (TypeError, AttributeError, IndexError):
            print('None!?')

def get_artist(track):
    try:
        for artist in track['track']['artists']:
            name = artist['name']
            trackArtists.append(name)
            print('; ', name)
            get_artist_genre(name)
            break

    except (TypeError, AttributeError):
            print('None!?')


def get_tracks(pl_URI, tracks, count, offset):
    for track in spotify.playlist_tracks(pl_URI, offset=offset)['items']:
        try:
            track_uri = track['track']['uri']
            track_name = track['track']['name']
            result = track_name # , spotify.audio_features(track_uri)
            tracks.append(result)
            print(track['track']['name'])
            get_artist(track)
            count += 1
            
        except (TypeError, AttributeError):
            print('None!?')

    return count

def organize():

    # issue: list of items, for each item in list --> check corresponding object's genre, store object if object property matches...
    # potential solution: create 2d array where rows are duplicated from other list and columns are empty
    # POSSIBLE SOLUTION ATM: go through every single artist first then create dict and store all genres in keys, the value will then have songs appended as the sorting is being done

    for i in range(target):
        print(tracks[i], ' : ',trackGenres[i])
        for j in range(len(genreList)):
            if genreList[j] == trackGenres[i]:
                songDict[genreList[j]].append(tracks[i])
        

def run(target, count, offset):

    if count <= target:
        count = get_tracks('2yD67LQ7HpqLKUQKR5JTet', tracks, count, offset) # 4tsG3tuHtK3S3GoRCAl8n1 26jDYsxAgRqpOIRovfWU9L
        offset += 100
        run(target, count, offset)
    else:
        print('------------------DONE------------------')
        print(genreList)
        print()

tracks = []
trackGenres = []
trackArtists = []
genreList = []

songDict = {}

target = 70 # int(input('Enter total # of songs in playlist: '))
run(target=target, count=1, offset=0)
f.close()

# for i in range(target):
#    print(tracks[i][0])

# print(tracks)

# artist_genres = (spotify.artist(artist_id='0Y5tJX1MQlPlqiwlOH1tJY'))['genres']
# print(artist_genres)

organize()

print(songDict)