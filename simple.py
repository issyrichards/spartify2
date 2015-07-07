from flask_oauthlib.client import OAuth
from flask import session
from flask import redirect

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth()
spotify = oauth.remote_app(
    'spotify',
    consumer_key='66dfb3e0319e450d8de499b92ee09eb8',
    consumer_secret='2687b3585918493c9b9d53ab86ac5921',
    request_token_params={'scope':'playlist-modify-public'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='/api/token',
    authorize_url='https://accounts.spotify.com/authorize')

@spotify.tokengetter
def get_spotify_token(token=None):
    return session.get('spotify_token')

@app.route('/login')
def login():
    return spotify.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))

@app.route('/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['spotify_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

if __name__ == '__main__':
    app.run()
