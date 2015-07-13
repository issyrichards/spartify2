from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

@app.route('/')
def spartify():
	return render_template('spartifymultiple.html')

if __name__ == '__main__':
    app.run()