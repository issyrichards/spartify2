#build up other functions (which don't need authentification) to replace the track ID's. Add in user_playlist_reorder_tracks(user, playlist_id, range_start, insert_before, range_length=1, snapshot_id=None). Need to find a way of iterating over multiple names.

from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

import pprint
import sys
import spotipy
import spotipy.util as util

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

@app.route('/')
def login():
	scope = 'playlist-modify-public'
	username = raw_input('>')
	token = util.prompt_for_user_token(username, scope, '66dfb3e0319e450d8de499b92ee09eb8', '60c4e23940b14a5a9a4f160b66bae738', 'http://localhost:5000/callback/')
	print 'after token'

	if token:
		print 'with token'
		name = raw_input('>>')
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
		playlists = sp.user_playlist_create(username,name, public=True)
		songs = sp.user_playlist_add_tracks(username, playlists['id'], ['0eGsygTp906u18L0Oimnem'])
		pprint.pprint(songs)
		return render_template('thanks.html')

	else:
		print "Can't get token for", username
		return render_template('thanks.html')

@app.route('/callback/')
def callback():
	print 'callback'
	return render_template('thanks.html')

if __name__ == '__main__':
    app.run()