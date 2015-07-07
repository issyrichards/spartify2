from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth


import sys
import spotipy
import spotipy.util as util

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
scope = 'user-library-read'

@app.route('/')
def login():
	username = raw_input('>')
	token = util.prompt_for_user_token(username, scope, '66dfb3e0319e450d8de499b92ee09eb8', '60c4e23940b14a5a9a4f160b66bae738', 'http://localhost:5000/callback/')
	print 'after token'

	if token:
		print 'with token'
		sp = spotipy.Spotify(auth=token)
		results = sp.current_user_saved_tracks()
		for item in results['items']:
			track = item['track']
			print track['name'] + ' - ' + track['artists'][0]['name']
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