import pytest
from fastapi.testclient import TestClient
from src.app import app  

client = TestClient(app)

@pytest.mark.parametrize("size,expected_price", [
    (10.0, 200.0),
    (20.0, 400.0),
    (30.0, 600.0),
])

def test_predict_price(size, expected_price):
    response = client.post("/predict", json={"size": size})
    assert response.status_code == 200
    assert "predicted_price" in response.json()
    assert response.json()["predicted_price"] > expected_price

def test_read_predictions():
    response = client.get("/predictions")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_predict_price_invalid_size():
    response = client.post("/predict", json={"size": -10.0})  # Valor inválido
    assert response.status_code == 422  # Verifica que se reciba un error de validación
    assert "detail" in response.json()
    
@pytest.mark.xfail(reason="Simulación de error")
def test_error_predict_price():
    response = client.post("/predict", json={"size": "error"})
    assert response.status_code == 200
    