import pylast
import os
import spot

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']

username = os.environ['username']
password_hash = pylast.md5(os.environ['password_hash'])

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

artist = input('Enter artist name: ') #'aries'
song = input('Enter song name: ') #'sayonara'

track = network.get_track(artist, song)

try:
    genre = track.get_top_tags()[0][0]
except(IndexError):
    genre = spot.get_artist_genre(artist)[0]

print('Track --> ', track, '\nGenre --> ', genre)