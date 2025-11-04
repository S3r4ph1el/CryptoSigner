from config import DATA_DIR
from routes import routes
import os, flask

app = flask.Flask(__name__)
app.register_blueprint(routes)

@app.route('/', methods=['GET'])
def home():
    return flask.send_from_directory('templates', 'signer.html')

@app.route('/check.html', methods=['GET'])
def check_signature():
    return flask.send_from_directory('templates', 'check.html')

if __name__ == '__main__':

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    app.run(debug=True) # Pode ser setado para False para menor verbosidade