from app import app
from services import (
    get_latest_bitcoin_price,
    get_average_bitcoin_price
)


@app.route('/', methods=['GET'])
def bitcoin_latest():
    """Endpoint to get the latest Bitcoin price."""
    return get_latest_bitcoin_price()


@app.route('/average', methods=['GET'])
def bitcoin_average():
    """Endpoint to get the 10-minute average Bitcoin price."""
    return get_average_bitcoin_price()


@app.route('/live', methods=['GET'])
def liveness_probe():
    """Kubernetes liveness probe."""
    return {"status": "Service A is alive"}, 200


@app.route('/ready', methods=['GET'])
def readiness_probe():
    """Kubernetes' readiness probe."""
    return {"status": "Service A is ready"}, 200
