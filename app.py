from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

import sorter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tracks_by_genre = None

    if request.method == 'POST':
        playlist_id = request.form.get('playlist_id')
        username = request.form.get('username')

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
                                                    scope="playlist-modify-public",
                                                    username=username))

        if playlist_id:
            # Call your sorter.py functions and get the data
            tracks_by_genre = sorter.organize_playlist_by_genre(playlist_id, sp, username)

    return render_template('index.html', tracks_by_genre=tracks_by_genre)

if __name__ == '__main__':
    app.run()
