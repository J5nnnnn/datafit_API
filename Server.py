from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import numpy as np
import json
from model_load import load_model, payload_preprocessing

# Start Flask app
app = Flask(__name__)
api = Api(app)

# Parser for payload data; The key for products name will be 'data'
# reqparse does not work well when loading a list of string

# parser = reqparse.RequestParser()
# parser.add_argument('data')


class Classifer(Resource):
    def post(self):
        if request.is_json:
            args = request.get_json()
            print(args)
            products_name = args['data']
            print(products_name)
            print(payload_preprocessing(model))
            return "success!"
        else:
            return "Invalid payload format", 400


print("outside run!!")

api.add_resource(Classifer, '/classify')


# test purpose, will delete after
@app.route('/')
def hello():
    return "hello, world"


if __name__ == '__main__':
    model = load_model()
    print("main run")
    app.run(port=8000)
