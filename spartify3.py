import sys
import spotipy
import spotify.util as util

scope = 'playlist-modify-public'

SPOTIFY_APP_ID = '66dfb3e0319e450d8de499b92ee09eb8'
SPOTIFY_APP_SECRET = '2687b3585918493c9b9d53ab86ac5921'
REDIRECT_URI = 'localhost:5000/login/authorized'

token = util.prompt_for_user_token(username, scope, SPOTIFY_APP_ID, SPOTIFY_APP_SECRET, REDIRECT_URI)