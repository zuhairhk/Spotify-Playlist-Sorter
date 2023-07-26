import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

file = open("out.txt","w+")

# set up Spotify client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# function to retrieve track genres
def get_track_genres(track_id):
    # retrieve track info
    try:
        track_info = sp.track(track_id)
        # retrieve artist info
        artist_info = sp.artist(track_info['artists'][0]['id'])
        # return genres associated with the track's artist
        return artist_info['genres']
    except:
        print('Some none type error for the track_id or smt')
        return 'blank'
    

# function to retrieve playlist tracks and organize by genre
def organize_playlist_by_genre(playlist_id):
    # create dictionary to store tracks by genre
    tracks_by_genre = {}
    # retrieve playlist tracks
    playlist_tracks = sp.playlist_tracks(playlist_id)
    # iterate over each page of tracks in the playlist
    while playlist_tracks:
        # iterate over each track in the page
        for track in playlist_tracks['items']:
            # retrieve track info
            try:
                track_id = track['track']['id']
                track_name = track['track']['name']
            except:
                track_id = '0tMMPZEt6Gyrl9FI8zSicm'
                track_name = 'Glue Song'
            
            print(track_name)
            # retrieve track genres
            track_genres = get_track_genres(track_id)
            # iterate over each genre associated with the track
            for genre in track_genres:
                # check if genre already exists in dictionary
                if genre not in tracks_by_genre:
                    # if genre doesn't exist, create new list for genre
                    tracks_by_genre[genre] = []
                # add track to genre's list
                tracks_by_genre[genre].append(track_name)
        # check if there are more pages
        playlist_tracks = sp.next(playlist_tracks) if playlist_tracks['next'] else None
    file.write(str(tracks_by_genre))
    print(tracks_by_genre)
    '''
    # create new playlist for each genre and add tracks to playlist
    for genre in tracks_by_genre:
        # create new playlist with genre name
        playlist_name = f"{genre} Playlist"
        sp.user_playlist_create(user='', name=playlist_name)
        # retrieve playlist ID for newly created playlist
        playlist_id = sp.current_user_playlists()['items'][0]['id']
        # add tracks to playlist
        track_ids = []
        for track in tracks_by_genre[genre]:
            results = sp.search(track, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                track_ids.append(track_uri)
        #sp.playlist_add_items(playlist_id, track_ids)
        print(playlist_id, track_ids)
    '''



organize_playlist_by_genre('26jDYsxAgRqpOIRovfWU9L') #YEAH=26jDYsxAgRqpOIRovfWU9L, smtiforgot=2yD67LQ7HpqLKUQKR5JTet
