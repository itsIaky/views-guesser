from flask_bootstrap import Bootstrap5
from flask import Flask           
from flask import Flask, render_template
from flask import request
import time
import math
from Service import *

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def run_predict():
    print(request.json)
    response = app.response_class(
        response={"views":"1000"},
        status=200,
        mimetype='application/json'
    )
    #time.sleep(5)
    print(request.json)
    error = Predicter().check(request.json)
    if(error["error"] == True):
        return error
    
    views = int(Predicter().predict(request.json)[0])
    return {
        "error" : False,
        "views" : views,
    }
    #return ToDoService().create(request.get_json())

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
