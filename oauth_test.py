from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'random secret'

#oauth config
oauth = OAuth(app)
google = oauth.register(
    name= 'google',
    client_id= '822187027449-skifkgv7dc9cgpdieu68d7ikj3bbcp6s.apps.googleusercontent.com',
    client_secret= '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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params= None,
    authorize_url= 'https://accounts.google.com/o/oauth2/auth',
    authorize_params= None,
    api_base_url= 'https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'profile email'},
)

@app.route('/')
def hello_world():
    email = dict(session).get('email', None)
    return f'Hello, {email}!'

# the first route when logging in
@app.route('/login')
def login():
    google = oauth.create_client('google') # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# the route clients get redirected to
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')