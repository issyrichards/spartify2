
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth, OAuthException
import spotipy
import pprint
import sys
import spotipy.util as util


sp = spotipy.Spotify()

pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

def get_artist_id(name):
	results = sp.search(q=name, limit=1, offset=0, type='artist')
	return results['artists']['items'][0]['id']

def get_artist_top_tracks(name):
	results = get_artist_id(name)
	tracks = sp.artist_top_tracks(results)
	return tracks

def get_top_five(name):
	results = get_artist_top_tracks(name)
	tracks = results['tracks']
	return tracks[0:5]

def get_track_id(name):
	tracks = get_top_five(name)
	ids = []
	for i in tracks:
		ids.append(i['id'])
	return ids

def create_playlist(username, playlist_name, name):
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, '66dfb3e0319e450d8de499b92ee09eb8', '60c4e23940b14a5a9a4f160b66bae738', 'http://localhost:5000/callback/')
    
    sp = spotipy.Spotify(auth=token)
    sp.trace = False	
    results = sp.user_playlist_add_tracks(username, playlist_name, get_track_id(name))
    return results

@app.route('/')
def index():
    return render_template('spartify.html')

@app.route('/', methods=['POST'])
def sign_up():
	form_data = request.form
	artist = form_data['artist']
	playlist_name = form_data['playlist_name']
	username = form_data['username']
	create_playlist(username, playlist_name, artist)
	return render_template('thanks.html')

@app.route('/')
def callback():
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run()


