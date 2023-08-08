import pytest
import json
import jwt
from Server import app, db, User
from werkzeug.security import generate_password_hash
import json
import uuid
from datetime import datetime, timedelta

# Utility function to create a user
def create_user(email, password):
    user = User(public_id = str(uuid.uuid4()),
                name = 'Test',
                email = email,
                password = generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user

# Function to create a token for a user
def get_token(user):
    token = jwt.encode({
        'public_id': user.public_id,
        'exp' : datetime.utcnow() + timedelta(minutes = 30)
    }, app.config['SECRET_KEY'])
    return token.decode('UTF-8')

# Create app context for each test
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client, app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_success_signup(client):
    response = client.post('/signup', data=dict(name='Test123', email='testimonial@gmail.com', password='test1234'))
    assert response.status_code == 201
    
def test_long_username_signup(client):
    response = client.post('/signup', data=dict(name='T'*21, email='test@test.com', password='test'))
    assert response.status_code == 400

def test_short_password_signup(client):
    response = client.post('/signup', data=dict(name='Test', email='test@test.com', password='short'))
    assert response.status_code == 400

def test_long_password_signup(client):
    response = client.post('/signup', data=dict(name='Test', email='testim222l@gmail.com', password='l'*21))
    assert response.status_code == 400

def test_duplicate_email_signup(client):
    # Sign up the first user with a specific email
    response1 = client.post('/signup', data=dict(name='Test123', email='duplicate@gmail.com', password='test56756'))
    assert response1.status_code == 201

    # Try to sign up again with the same email
    response2 = client.post('/signup', data=dict(name='Test123', email='duplicate@gmail.com', password='test56756'))
    assert response2.status_code == 202

def test_success_login(client):
    create_user('test_login@test.com', 'test')
    response = client.post('/login', data=dict(email='test_login@test.com', password='test'))
    assert response.status_code == 201
    
def test_invalid_login(client):
    response = client.post('/login', data=dict(email='notexist@test.com', password='test'))
    assert response.status_code == 401

def test_wrong_password_login(client):
    create_user('test_wrong_password@test.com', 'test')
    response = client.post('/login', data=dict(email='test_wrong_password@test.com', password='wrong'))
    assert response.status_code == 403

def test_missing_token_user(client):
    response = client.get('/user')
    assert response.status_code == 401
    
def test_invalid_token_user(client):
    response = client.get('/user', headers={'x-access-token': 'invalid_token'})
    assert response.status_code == 401

def test_get_all_users(client):
    user = create_user('test_get_all_users@test.com', 'test')
    token = get_token(user)
    response = client.get('/user', headers={'x-access-token': token})
    assert response.status_code == 200

def test_classifier(client):
    user = create_user('test_classifier@test.com', 'test')
    token = get_token(user)
    response = client.post('/classify', headers={'x-access-token': token}, json={'data': ['product1', 'product2']})
    assert response.status_code == 200

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'hello, world'
