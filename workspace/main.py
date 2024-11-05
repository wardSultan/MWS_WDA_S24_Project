from flask import Flask
from flask_cors import CORS
from controllers import data_controller

app = Flask(__name__)
CORS(app)

app.register_blueprint(data_controller.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
