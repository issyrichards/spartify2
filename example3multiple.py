#build up other functions (which don't need authentification) to replace the track ID's. Add in user_playlist_reorder_tracks(user, playlist_id, range_start, insert_before, range_length=1, snapshot_id=None). Need to find a way of iterating over multiple names.

from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

import pprint
import sys
import spotipy
import spotipy.util as util
import random
from random import randint

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

sp = spotipy.Spotify()

pp = pprint.PrettyPrinter(indent=4)

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

@app.route('/')
def initiate():
	return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login():
	scope = 'playlist-modify-public'

	form_data = request.form
	print form_data

	artists = []

	for key in form_data:
		if key != 'username' and key != 'playlist_name':
			if form_data[key] != '':
				artists.append(form_data[key])

	print artists

	playlist_name = form_data['playlist_name']
	username = form_data['username']

	token = util.prompt_for_user_token(username, scope, '66dfb3e0319e450d8de499b92ee09eb8', '60c4e23940b14a5a9a4f160b66bae738', 'http://localhost:5000/callback/')
	print 'after token'

	if token:
		print 'with token'
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
		playlists = sp.user_playlist_create(username,playlist_name, public=True)
		for artist in artists:
			songs = sp.user_playlist_add_tracks(username, playlists['id'], get_track_id(artist))
		
		for x in range(0, (len(artists)*5)-1):
			reorder = sp.user_playlist_reorder_tracks(username, playlists['id'], x, random.randint(0, (len(artists)*5)))

		pprint.pprint(reorder)
		return render_template('thanks.html')

	else:
		print "Can't get token for", username
		return render_template('thanks.html')

@app.route('/login')
def form():
	return render_template('spartifymultiple.html')

@app.route('/callback/')
def callback():
	print 'callback'
	return render_template('thanks.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)