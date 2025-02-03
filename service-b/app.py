from flask import Flask
from config import Config

app = Flask(__name__)


if __name__ == '__main__':
    from routes import *
    app.run(host=Config.base_url, port=Config.base_port, debug=True)
