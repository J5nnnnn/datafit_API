from flask import Flask, request, jsonify, make_response, render_template, flash, g, redirect, url_for, session
from flask_restful import Api, Resource, reqparse
#import numpy as np
import json
from flask_sqlalchemy import SQLAlchemy
import uuid 
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from email_validator import validate_email, EmailNotValidError
import time

from model_load import load_model, payload_preprocessing, load_model_sub


# Start Flask app
app = Flask(__name__)
api = Api(app)

# flask imports

# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)


# Database ORMs
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(70), unique=True)
	password = db.Column(db.String(80))


# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return {'message' : 'Token is missing !!'}, 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = User.query\
				.filter_by(public_id = data['public_id'])\
				.first()
    		# store data shared during a context 
			g.current_user = current_user  # store the current user in g
		except:
			return {
				'message' : 'Token is invalid !!'
			}, 401
		# returns the current logged in users context to the routes
		return f(current_user, *args, **kwargs)

	return decorated


# User Database Route
# this route sends back list of users
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
	# querying the database
	# for all the entries in it
	users = User.query.all()
	# converting the query objects
	# to list of jsons
	output = []
	for user in users:
		# appending the user data json
		# to the response list
		output.append({
			'public_id': user.public_id,
			'name' : user.name,
			'email' : user.email
		})

	return jsonify({'users': output})


# route for logging user in
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		# creates dictionary of form data
		auth = request.form

		if not auth or not auth.get('email') or not auth.get('password'):
			# returns 401 if any email or / and password is missing
			return make_response(
				'Could not verify',
				401,
				{'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
			)

		user = User.query\
			.filter_by(email = auth.get('email'))\
			.first()

		if not user:
			# returns 401 if user does not exist
			return make_response(
				'Could not verify',
				401,
				{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
			)

		if check_password_hash(user.password, auth.get('password')):
			# generates the JWT Token
			token = jwt.encode({
				'public_id': user.public_id,
				'exp' : datetime.utcnow() + timedelta(minutes = 30)
			}, app.config['SECRET_KEY'])

			return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
		# returns 403 if password is wrong
		return make_response(
			'Could not verify',
			403,
			{'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
		)
	return render_template('login.html')

# signup route
@app.route('/signup', methods =['GET', 'POST'])
def signup():
	if request.method == 'POST':
		# creates a dictionary of the form data
		data = request.form

		# gets name, email and password
		name, email = data.get('name'), data.get('email')
		password = data.get('password')
    

		try:                                          
			v = validate_email(email)
			email = v["email"]
		except EmailNotValidError as e:
			return make_response(str(e), 400)

		# Username length validation
		if len(name) < 3 or len(name) > 20:
			return make_response('Username must be between 3 and 20 characters.', 400)

		# Password length validation
		if len(password) < 8 or len(password) > 20:
			return make_response('Password must be between 8 and 20 characters.', 400) 


		# checking for existing user by email
		user_with_email = User.query\
		.filter_by(email=email)\
		.first()

		# checking for existing user by name
		user_with_name = User.query\
		.filter_by(name=name)\
		.first()

		if user_with_email or user_with_name:
			# returns 202 if user already exists
			# return make_response('User with this email or name already exists. Please change.', 202)
			flash('User already exists. Please log in.')
			return redirect(url_for('login'))
		else:
			# database ORM object
			user = User(
				public_id=str(uuid.uuid4()),
				name=name,
				email=email,
				password=generate_password_hash(password, method='sha256')
			)
			# insert user
			db.session.add(user)
			db.session.commit()
		
			flash('Account created successfully. Please log in.')
			return redirect(url_for('login'))
	return render_template('signup.html')


# Parser for payload data; The key for products name will be 'data'
# reqparse does not work well when loading a list of string

# parser = reqparse.RequestParser()
# parser.add_argument('data')


class Classifer(Resource):
    # decorator for classifying
	@token_required
	def post(self, current_user):
		current_user = g.current_user  # access the current user with g.current_user
		if request.is_json:
				args = request.get_json()
				products_name = [x.lower() for x in args['data']]
				print(products_name)

				t1 = time.time()

				res = payload_preprocessing(model, model_sub, products_name)
				t2 = time.time()
				print(res)
				return json.dumps(res)
		else:
				return "Invalid payload format", 400



api.add_resource(Classifer, '/classify')

@app.route('/classify', methods=['GET','POST'])
# @token_required
def classify():
	if request.method == 'POST':
		try:
			# Call the classifier logic here
			# This could involve using a machine learning model, processing data, etc.
			result = "Your classification result"  # Modify this with your actual result
			return jsonify({'result': result})
		except Exception as e:
			return jsonify({'error': 'An error occurred'}), 500
	else:
		return render_template('classify.html')


# test purpose, will delete after
@app.route('/')
def index():
	return render_template('index.html')

# Route for the profile page
@app.route('/profile')
@token_required
def profile(current_user):
    return render_template('profile.html', current_user=current_user)

@app.route('/logout')
def logout():
    # Perform logout actions, such as clearing session data
    # For example:
    session.clear()
    # Or remove authentication, etc.

    # Redirect to a different page after logout
    return redirect(url_for('index'))  # 'home' is the endpoint of your home page

with app.app_context():
    db.create_all()

if __name__ == '__main__':

    model = load_model()
    model_sub = load_model_sub()
    print("main run")
    app.run(port=8000)

'''
have a real db, so we could set up some schema for data format
db:
	1. username should be unique
	2. username not email, should be alert
	3. 

response code for 400level?

token encryption

GPU to improve the model speed


'''
