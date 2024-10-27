from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import joblib
import os
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Summary, Histogram

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
house_size_histogram = Histogram('house_size', 'Distribución de los tamaños de las casas solicitadas', buckets=[50, 100, 150, 200, 250, 300, 350, 400])

# Definir el esquema de entrada
class SizeInput(BaseModel):
    size: float

# Definir el modelo para la respuesta de la predicción
class PredictionResponse(BaseModel):
    id: str
    size: float
    predicted_price: float

# Endpoint para predecir el precio
@app.post("/predict", response_model=PredictionResponse)
async def predict_price(input_data: SizeInput):
    try:
        # Incrementa el contador de solicitudes
        prediction_requests.inc()
        
        # Registra el tamaño de la casa en el histograma
        house_size_histogram.observe(input_data.size)
        
        # Mide el tiempo de procesamiento
        with prediction_time.time():
            size = input_data.size
            predicted_price = model.predict([[size]])[0]
        
        # Guardar el resultado en la base de datos
        prediction_data = {
            "size": size,
            "predicted_price": predicted_price
        }
        result = predictions_collection.insert_one(prediction_data)
        prediction_data['id'] = str(result.inserted_id)  # Agregar el id generado

        return PredictionResponse(**prediction_data)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint para obtener todas las predicciones
@app.get("/predictions", response_model=list[PredictionResponse])
async def get_predictions():
    predictions = list(predictions_collection.find({}, {'_id': 0}))  # Obtener todos los documentos, sin el _id
    for prediction in predictions:
        prediction['id'] = str(prediction.get('id'))  # Convertir el ID a string
    return predictions

# Endpoint de health check
@app.get('/health')
async def health_check():
    return {"status": "OK"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
