from flask import Flask, request, url_for, redirect, session, render_template, jsonify
from flask_restful import Api, Resource, reqparse
import numpy as np
import json
# from model_load import load_model, payload_preprocessing
from authlib.integrations.flask_client import OAuth

# Start Flask app
app = Flask(__name__)
app.secret_key = 'random secret'
api = Api(app)

# Parser for payload data; The key for products name will be 'data'
# reqparse does not work well when loading a list of string

# parser = reqparse.RequestParser()
# parser.add_argument('data')


class Classifer(Resource):
    def post(self):
        if request.is_json:
            args = request.get_json()
            products_name = args['data']
            print(products_name)
            # res = payload_preprocessing(model, products_name)
            # print(res)
            return json.dumps(products_name)
        else:
            return "Invalid payload format", 400


print("outside run!!")

api.add_resource(Classifer, '/classify')

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
def index():
    return render_template('index.html')

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
    resp = google.get('userinfo') #use get function to retrieve user info, including email and other details
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email'] # stores emails in userinfo into session
    return redirect('/classify')

@app.route('/classify', methods=['GET','POST'])
def classify():
    if 'email' not in session:
        return render_template('login.html')  # Correct the template name
    else:
        # # Todo: call the api by clicking the button
        # if request.is_json:
        #     args = request.get_json()
        #     products_name = args['data']
        #     # Now, make use of 'products_name' and call the Classifier API
        #     # For example, you can call the API using the 'requests' library
        #     # response = requests.post('http://localhost:8000/classify', json=products_name)
        #     # Do something with the response if needed and return JSON data
        #     # return jsonify(response.json())
        #     # For now, let's return a sample response
        #     return jsonify({'result': 'Sample response for ' + products_name})
        # else:
        #     return "Invalid payload format", 400
        return render_template('classify.html')
    

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



if __name__ == '__main__':
    # model = load_model()
    print("main run")
    app.run(port=8000)
