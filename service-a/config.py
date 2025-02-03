import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    base_url: str = '0.0.0.0'
    base_port: int = 80
    coinmarketcap_api_key: str = os.getenv("COINMARKETCAP_API_KEY")
    coinmarketcap_api_url: str = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    symbol: str = 'BTC'
    currency: str = 'USD'

    @staticmethod
    def get_headers():
        return {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': Config.coinmarketcap_api_key
        }

    @staticmethod
    def get_params():
        return {
            'symbol': Config.symbol,
            'convert': Config.currency
        }
