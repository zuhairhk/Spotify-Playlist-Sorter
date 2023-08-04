import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

# IMPLEMENT GETTERS AND SETTERS IN CLEANUP
tracks_by_genre = {} # scuffed sol. fix after

def get_track_genres(track_id, sp):
    try:
        track_info = sp.track(track_id)
        artist_info = sp.artist(track_info['artists'][0]['id'])
        return artist_info['genres']
    except:
        print('Some none type error for the track_id or smt')
        return 'blank'
    

def organize_playlist_by_genre(playlist_id, sp, username):
    i = 1
    playlist_tracks = sp.playlist_tracks(playlist_id)

    while playlist_tracks:
        for track in playlist_tracks['items']:
            try:
                track_id = track['track']['id']
                track_name = track['track']['name']
            except:
                track_id = '0tMMPZEt6Gyrl9FI8zSicm'
                track_name = 'Glue Song'
            
            print(i, ': ', track_name)
            i += 1
            
            track_genres = get_track_genres(track_id, sp)
            
            for genre in track_genres:
                if genre not in tracks_by_genre:
                    tracks_by_genre[genre] = []
                tracks_by_genre[genre].append(track_name)

        playlist_tracks = sp.next(playlist_tracks) if playlist_tracks['next'] else None

    return tracks_by_genre

    #file.write(str(tracks_by_genre))
    print(tracks_by_genre)

    updated_tbr = select_playlists(tracks_by_genre)
    create_playlists(updated_tbr, sp, username)

def select_playlists(tracks_by_genre):
    for genre in tracks_by_genre:
        print(genre)
    selected_genre = input('Enter genre to make a playlist off: ')

    new_tbr = {}
    if selected_genre in tracks_by_genre:
        new_tbr[selected_genre] = tracks_by_genre[selected_genre]

    return new_tbr


def create_playlists(tracks_by_genre, sp, username):
    for genre in tracks_by_genre:
        playlist_name = f"{genre} Playlist"
        sp.user_playlist_create(username, name=playlist_name)
        playlist_id = sp.current_user_playlists()['items'][0]['id']
        track_ids = []
        for track in tracks_by_genre[genre]:
            results = sp.search(track, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                track_ids.append(track_uri)
        sp.playlist_add_items(playlist_id, track_ids)
        print(playlist_id, track_ids)


def main(playlist_id, username):
    # print("Please enter your Spotify credentials:")

    playlist_id = playlist_id.split('/')[-1]
    playlist_id = playlist_id.split('?')[0]


    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                    redirect_uri='http://localhost:5000/callback',
                                                    scope="playlist-modify-public",
                                                    username=username))
    
    if playlist_id == None:
        print('Error handling here after')
    
    # 6PfP2dLuEjryzCK9Fw4b1M YEAH=26jDYsxAgRqpOIRovfWU9L, smtiforgot=2yD67LQ7HpqLKUQKR5JTet '03JS3MM4SVhnODKMJOV5Mt' 6yviE4o9M6uYe9OkzqYlZZ
    # https://open.spotify.com/playlist/26jDYsxAgRqpOIRovfWU9L?si=05f6b8259cdb4189
    # https://open.spotify.com/playlist/6yviE4o9M6uYe9OkzqYlZZ?si=05f6b8259cdb4189

    result = organize_playlist_by_genre(playlist_id, sp, username)
    print(result)

if __name__ == "__main__":
    main('6yviE4o9M6uYe9OkzqYlZZ', 'zuhairhk')
