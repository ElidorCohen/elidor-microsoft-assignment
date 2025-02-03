from app import app


@app.route('/', methods=['GET'])
def hello():
    return {"status": "Hello from Service B"}, 200


@app.route('/live', methods=['GET'])
def liveness_probe():
    return {"status": "Service B is alive"}, 200


@app.route('/ready', methods=['GET'])
def readiness_probe():
    return {"status": "Service B is ready"}, 200
