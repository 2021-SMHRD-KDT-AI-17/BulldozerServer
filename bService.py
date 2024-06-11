from flask import Flask, request
from flask_restx import Api, Resource
from src import webCrawling as bwc
import time

app = Flask(__name__)
api = Api(app)

webi_dir = "./src/webimgs/"
@app.route('/mytest/')
def validateServer():
    parameter_dict = request.args.to_dict()
    if 'url' not in parameter_dict:
        return 'No parameter "url" provided'
    if 'id' not in parameter_dict:
        return 'No parameter "id" provided'
    url = "http://"+parameter_dict['url']
    uid= parameter_dict['id']
    response = bwc.driveropen(url,uid)
    return "테스트"+bwc.getTitlename

@app.route('/mytest2/')
def validateServer2():
    start = time.time()
    textlist=[]
    parameter_dict = request.args.to_dict()
    textlist=bwc.imageAnalyze(webi_dir+"samples/")
    print(f"{time.time()-start:.3f} sec")
    return "text2"


if __name__ == "__main__":
    app.run(debug=True, host='192.168.219.47', port=5000)