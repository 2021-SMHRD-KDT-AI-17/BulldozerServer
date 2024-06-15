from flask import Flask, request
from flask_restx import Api, Resource
from src import webCrawling as bwc

app = Flask(__name__)
api = Api(app)

webi_dir = "./src/webimgs/"

class ValidateServer(Resource):
    def post(self):
        if request.is_json:
            parameter_dict = request.get_json()
        else:
            parameter_dict = request.form.to_dict()

        if 'url' not in parameter_dict:
            return 'No parameter "url" provided', 400
        if 'id' not in parameter_dict:
            return 'No parameter "id" provided', 400

        url = parameter_dict['url']
        uid = parameter_dict['id']
        response = bwc.driveropen(url, uid)
        return response

# Register the resource
api.add_resource(ValidateServer, '/service/')

if __name__ == "__main__":
    app.run(debug=False, host='192.168.219.66', port=5000)