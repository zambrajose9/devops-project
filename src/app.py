from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
import joblib
import os
from time import time
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Summary

# Inicializar FastAPI
app = FastAPI()

# Cargar el modelo de regresión
model = joblib.load('src/model.pkl')

# Instrumentar la aplicación para Prometheus
Instrumentator().instrument(app).expose(app)

# Conexión a MongoDB
MONGO_URI = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo:27017/"
client = MongoClient(MONGO_URI)
db = client['mydatabase']
predictions_collection = db['predictions']

# Definir métricas personalizadas
prediction_requests = Counter('prediction_requests_total', 'Total de predicciones realizadas')
prediction_time = Summary('prediction_processing_time', 'Tiempo de procesamiento de predicción')

# Métricas personalizadas para los tres rangos de tamaño
predictions_0_50 = Counter('predictions_0_50_total', 'Total de predicciones con tamaño de casa entre 0 y 50')
predictions_50_75 = Counter('predictions_50_75_total', 'Total de predicciones con tamaño de casa entre 50 y 75')
predictions_75_plus = Counter('predictions_75_plus_total', 'Total de predicciones con tamaño de casa de 75 o más')

# Definir el esquema de entrada
class SizeInput(BaseModel):
    size: float = Field(..., gt=0) 

# Definir el modelo para la respuesta de la predicción
class PredictionResponse(BaseModel):
    id: str
    size: float
    predicted_price: float

# Endpoint para predecir el precio
@app.post("/predict", response_model=PredictionResponse)
async def predict_price(input_data: SizeInput):
    try:
        start_time = time()
        size = input_data.size
        predicted_price = model.predict([[size]])[0]

        # Guardar el resultado en la base de datos
        prediction_data = {
            "size": size,
            "predicted_price": predicted_price
        }
        result = predictions_collection.insert_one(prediction_data)
        prediction_data['id'] = str(result.inserted_id)

        # Actualizar las métricas personalizadas
        prediction_requests.inc()  # Incrementa el contador de predicciones
        prediction_time.observe(time() - start_time)  # Registra el tiempo de procesamiento

        # Actualizar métricas de acuerdo al tamaño
        if size <= 50:
            predictions_0_50.inc()
        elif 50 < size <= 75:
            predictions_50_75.inc()
        else:
            predictions_75_plus.inc()

        return PredictionResponse(**prediction_data)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint para obtener todas las predicciones
@app.get("/predictions", response_model=list[PredictionResponse])
async def get_predictions():
    predictions = list(predictions_collection.find({}, {'_id': 0}))
    for prediction in predictions:
        prediction['id'] = str(prediction.get('id'))
    return predictions

# Endpoint de health check
@app.get('/health')
async def health_check():
    return {"status": "OK"}

from fastapi.responses import JSONResponse

# Endpoint temporal para eliminar todas las predicciones
@app.delete("/predictions/clear")
async def clear_predictions():
    result = predictions_collection.delete_many({})
    return JSONResponse(content={"message": "Todas las predicciones han sido eliminadas", "deleted_count": result.deleted_count})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
