## Installation
### make sure to update your python version to at least 3.10

### environment
python3 -m venv env

source env/bin/activate

### Flask server
pip install -r requirements.txt

pip install email-validator

pip3 install flask

python3 -c "import flask; print(flask.__version__)"

pip3 install flask_restful

pip3 install numpy

### ML package
pip3 install translators --upgrade

pip3 install tensorflow

pip3 install tensorflow_hub

pip3 install tensorflow-text

pip3 install transformers

pip3 install datasets

### pytest
pip install pytest

pytest server_test.py

### server code running on 8000 since the default 5000 port on Mac OSX 12.X is already in use and may lead to 403 response error

## API Description
- Server:  
      - description: Data Fit predicting product category  
      url: http://127.0.0.1  
      port: 8000
- paths:
    - /signup
        - post:
            - requestBody(form-data):
               - key: name, value:[user_name]
               - key: email, value:[user_email]
               - key:password, value:[user_password]
            - response:
               - '202':
                   - description: User already exists
               - '201':
                   - description: Successfully registered
    - /login
        - post:
            - requestBody(form-data):
               - key: email, value:[user_email]
               - key:password, value:[user_password]
            - response:
               - '401':
                   - description: User does not exist or password is wrong
               - '201':
                   - description: Successfully logged in, returns a JWT token
                   - content:application/json
     - /user  
        - get:  
            - description: Get all users 
            - requestHeader(form-data):  
                - key: x-access-token, value:[jwt_token]
            - response:
               - '401':
                   - description: Token is missing or invalid
               - '200':
                   - description: Returns a list of all users
                   - content:application/json

     - /classify  
        - post:  
            - description: classify a list of products  
            - parameters:  
                - none
            - requestHeader(form-data):  
                - key: x-access-token, value:[jwt_token] 
            - requestBody:  
                - description: list of products name  
                - required: true  
                - content:  
                    - application/json  
            - response:  
                - '400':  
                    - description: Invalid payload format  
                - '200':
                    - description: list of the predicted category names
                    - content:
                        -  application/json  

## Postman test format
url: http://127.0.0.1:8000/classify  
POST  
Body: (in JSON)  
{  
  "data": ["apple", "banana", "orange"],  
  "comment": "test test"  
}

{
    "data" : ["uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid",
    "uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr", "kuaci rebo milk 13gr r2", "pristine 400ml", "komix kid"]
}


## Curl test format
curl -H 'Content-Type: application/json' \
    -d '{ "title":"foo","body":"bar", "id": 1, "data":["dunhill mild 16", "apache filter 12", "aqua 1500ml", "sasa 1kg", "close up 160gr", "gpu 60ml", "mama lemon 800ml"]}' \
    -X POST \
    http://127.0.0.1:8000/classify


curl -H 'Content-Type: application/json' \
    -d '{ "title":"foo","body":"bar", "id": 1, "data":["uj mimi full cream 125ml", "ladaku", "vixal 500ml", "aqua 330ml", "sprite 390ml", "koyo cabe", "abc mocca 27gr"]}' \
    -X POST \
    http://127.0.0.1:8000/classify

## Integratation with Bert Model
Currently, the model is loaded from the training weight. will work on to import the entire model for future work. 

## commentted out codes
Due to invalidation of Apple chip for some packages of Tensorflow, I comment out line 11, 177, 178, 195 in Server.py


