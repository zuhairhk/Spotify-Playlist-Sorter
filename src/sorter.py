import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

file = open("out.txt","w+")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_track_genres(track_id):
    try:
        track_info = sp.track(track_id)
        artist_info = sp.artist(track_info['artists'][0]['id'])
        return artist_info['genres']
    except:
        print('Some none type error for the track_id or smt')
        return 'blank'
    

def organize_playlist_by_genre(playlist_id):
    tracks_by_genre = {}
    playlist_tracks = sp.playlist_tracks(playlist_id)

    while playlist_tracks:
        for track in playlist_tracks['items']:
            try:
                track_id = track['track']['id']
                track_name = track['track']['name']
            except:
                track_id = '0tMMPZEt6Gyrl9FI8zSicm'
                track_name = 'Glue Song'
            
            print(track_name)
            
            track_genres = get_track_genres(track_id)
            
            for genre in track_genres:
                if genre not in tracks_by_genre:
                    tracks_by_genre[genre] = []
                tracks_by_genre[genre].append(track_name)

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


organize_playlist_by_genre('6PfP2dLuEjryzCK9Fw4b1M') #YEAH=26jDYsxAgRqpOIRovfWU9L, smtiforgot=2yD67LQ7HpqLKUQKR5JTet
