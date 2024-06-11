from flask import Flask, request
from flask_restx import Api, Resource
app = Flask(__name__)
api = Api(app)

@app.route('/mytest/')
def validateServer():
    return "테스트 성공"



if __name__ == "__main__":
    app.run(debug=True, host='192.168.219.44', port=5000)