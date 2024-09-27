from prometheus_client import Counter, start_http_server

REQUESTS = Counter('prediction_requests', 'Number of prediction requests')

def start_monitoring():
    start_http_server(8001)

def log_request():
    REQUESTS.inc()