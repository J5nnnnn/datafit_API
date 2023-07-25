## Installation
### make sure to update your python version to at least 3.10

### Flask server
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


### server code running on 8000 since the default 5000 port on Mac OSX 12.X is already in use and may lead to 403 response error

## API Description
- Server:  
      - description: Data Fit predicting product category  
      url: http://127.0.0.1  
      port: 8000
- paths:  
    - /classify  
        - post:  
            - description: classify a list of products  
            - parameters:  
                - none  
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

## Curl test format
curl -H 'Content-Type: application/json' \
    -d '{ "title":"foo","body":"bar", "id": 1, "data":["dunhill mild 16", "apache filter 12", "aqua 1500ml", "sasa 1kg", "close up 160gr"]}' \
    -X POST \
    http://127.0.0.1:8000/classify


## Integratation with Bert Model
Currently, the model is loaded from the training weight. will work on to import the entire model for future work
