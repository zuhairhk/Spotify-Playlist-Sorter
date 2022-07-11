import pylast
import os

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

artist = 'two door cinema club'
song = 'undercover martyn'

track = network.get_track(artist, song)

try:
    genre = track.get_top_tags()[0][0]
    print('Track --> ', track, '\nGenre --> ', genre)
except(IndexError):
    print('tuff index error yeah')
