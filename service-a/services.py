import requests
import time
import threading
from flask import jsonify
from config import Config
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bitcoin_prices = []


def fetch_bitcoin_price():
    """Fetches the latest Bitcoin price from CoinMarketCap API."""
    try:
        response = requests.get(Config.coinmarketcap_api_url, headers=Config.get_headers(), params=Config.get_params())
        response.raise_for_status()
        data = response.json()
        price = data['data'][Config.symbol]['quote'][Config.currency]['price']

        if price is not None:
            logging.info(f"Latest Bitcoin price: ${price:.5f}")
            print(f"Latest Bitcoin price: ${price:.5f}")
            bitcoin_prices.append(price)
            if len(bitcoin_prices) > 10:
                bitcoin_prices.pop(0)
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")


def calculate_average_price():
    """Calculates and prints the average price of Bitcoin over the last 10 minutes."""
    if len(bitcoin_prices) == 10:
        avg_price = sum(bitcoin_prices) / 10
        logging.info(f"Average Bitcoin price (last 10 min): ${avg_price:.2f}")
        print(f"Average Bitcoin price (last 10 min): ${avg_price:.2f}")


def bitcoin_price_scheduler():
    """Runs background scheduler to fetch Bitcoin price every minute and print the average every 10 minutes."""
    fetch_count = 0
    while True:
        fetch_bitcoin_price()
        fetch_count += 1

        if fetch_count == 10:
            calculate_average_price()
            fetch_count = 0

        time.sleep(60)


def start_bitcoin_price_scheduler():
    """Starts the scheduler in a separate thread."""
    thread = threading.Thread(target=bitcoin_price_scheduler, daemon=True)
    thread.start()


def get_latest_bitcoin_price():
    """Returns the most recent Bitcoin price."""
    if bitcoin_prices:
        return jsonify({'latest_bitcoin_price': bitcoin_prices[-1]}), 200
    return jsonify({'error': 'No data found'}), 404


def get_average_bitcoin_price():
    """Returns the 10-minute average Bitcoin price."""
    if len(bitcoin_prices) == 10:
        avg_price = sum(bitcoin_prices) / 10
        return jsonify({'average_bitcoin_price': avg_price}), 200
    return jsonify({'error': 'Not enough data to calculate average.'}), 500
