#This seems to be a mix of two different techniques, using spartify and oauth directly. Try and just call the creat playlist function more directly!)



from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth, OAuthException
import spotipy
import pprint
import sys
import spotipy.util as util


sp = spotipy.Spotify()

pp = pprint.PrettyPrinter(indent=4)

SPOTIFY_APP_ID = '66dfb3e0319e450d8de499b92ee09eb8'
SPOTIFY_APP_SECRET = 'b2584405c6ce40dcaffd82f8a4b50fc6'

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=SPOTIFY_APP_ID,
    consumer_secret=SPOTIFY_APP_SECRET,
    request_token_params={'scope':'playlist-modify-public'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)


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
    token = util.prompt_for_user_token(username, scope, '66dfb3e0319e450d8de499b92ee09eb8', '2687b3585918493c9b9d53ab86ac5921', 'http://www.spartify.co.uk')
    
    sp = spotipy.Spotify(auth=token)
    sp.trace = False	
    sp.user_playlist_add_tracks(username, playlist_name, get_track_id(name))
    print 'hi'
    return render_template('thanks.html')

@app.route('/')
def index():
    return redirect(url_for('spotify_authorized'))


@app.route('/login/authorized')
def spotify_authorized():
    return render_template('spartify.html')

@app.route("/login/authorized", methods=['POST'])
def sign_up():
    form_data = request.form
    artist = form_data['artist']
    playlist_name = form_data['playlist_name']
    username = form_data['username']
    return create_playlist(username, playlist_name, artist)
    
    

if __name__ == '__main__':
    app.run()


