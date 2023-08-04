from flask import Flask, render_template, request, session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

import sorter

app = Flask(__name__)
app.secret_key = "OOPpain" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select/', methods=['GET', 'POST'])
def select():

    if request.method == 'POST':
        playlist_id = request.form.get('playlist_id')
        username = request.form.get('username')
        session['username'] = username

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                    redirect_uri='http://localhost:5000/callback',
                                                    scope="playlist-modify-public",
                                                    username=username))

        if playlist_id:
            tracks_by_genre = sorter.organize_playlist_by_genre(playlist_id, sp, username)

    return render_template('select.html', tracks_by_genre=tracks_by_genre)

@app.route('/selected/', methods=['POST'])
def selected():
    username = session.get('username')
    print(username + "\n\n\n")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                    redirect_uri='http://localhost:5000/callback',
                                                    scope="playlist-modify-public",
                                                    username=username))

    # Get the selected genres from the form
    selected_genres = request.form.getlist('selected_genres')
    print(selected_genres)  # Print the selected genres to the console

    new_tbr = {}
    for selected_genre in selected_genres:
        if selected_genre in sorter.tracks_by_genre:
            new_tbr[selected_genre] = sorter.tracks_by_genre[selected_genre]

    sorter.create_playlists(new_tbr, sp, username)
    sorter.tracks_by_genre = {}

    return f'Playlist(s) created for:\n{new_tbr}'

if __name__ == '__main__':
    app.run(port=5001)
