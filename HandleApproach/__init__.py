import azure.functions as func
import pandas as pd
from flask import Flask, render_template, request
import os


app = Flask(__name__)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

STATIC_FOLDER ='static/'
MODEL_FOLDER = STATIC_FOLDER + 'models/'
DATA_FOLDER = STATIC_FOLDER + 'data/'

@app.before_first_request
def load__data():
    """
    Load predicted data
    :return: model (global variable)
    """
    print('[INFO] Predicted data Loading ........')
    #global model
    #model = load_model(MODEL_FOLDER + 'bidirectional_lstm_with_return_sequences_on_embedded_heroku')
    #print('[INFO] : Model loaded')
    global data
    data = pd.read_pickle(os.path.join(os.curdir, 'static\\data\\prediction_content_based.pickle'))

def predict(user_id, rs_type="content_based"):
    # Prediction:
    result_pred = list(data[data["user_id"]==str(user_id)]["article_id"]) 
    return result_pred

# Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_id = request.form["user_id"]
        print( user_id)
        #rs_type = request.form["rs_type"]
        result_pred = predict(user_id)

        return render_template('index.html', data=data, userId=user_id, result_pred=result_pred, predict=True)
    else:
        return render_template('index.html', data=data, predict=False)

# Hello Page
@app.route("/hello/<name>", methods=['GET'])
def hello(name: str):
    return f"hello {name}"
