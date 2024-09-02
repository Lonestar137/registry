from fastapi import FastAPI, Response
from prometheus_client import Counter, Gauge, generate_latest
from random import randint

app = FastAPI()

# Prometheus metrics
request_counter = Counter('requests_total', 'Total requests')
response_size_gauge = Gauge('response_size_bytes', 'Response size in bytes')


# Arbitrary data endpoint
@app.get("/data")
def read_data():
    request_counter.inc()
    data = {
        "id": randint(1, 100),
        "name": f"User {randint(1, 100)}",
        "age": randint(18, 65)
    }
    response_size_gauge.set(len(str(data)))
    return data


# Health check endpoint
@app.get("/health")
def read_health():
    request_counter.inc()
    return {"status": "ok"}


# Prometheus metrics endpoint
@app.get("/metrics")
def read_metrics():
    request_counter.inc()
    return Response(content=generate_latest(), media_type="text/plain")


# To run:
# pip install fastapi uvicorn prometheus-client
# uvicorn main:app --host 0.0.0.0 --port 8000
