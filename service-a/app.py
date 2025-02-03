from flask import Flask
from config import Config
from services import start_bitcoin_price_scheduler

app = Flask(__name__)

start_bitcoin_price_scheduler()

if __name__ == '__main__':
    from routes import *
    app.run(host=Config.base_url, port=Config.base_port, debug=False)
