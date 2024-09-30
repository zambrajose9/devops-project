from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import joblib
import os

# Cargar el modelo entrenado
model = joblib.load('src/model.pkl')

# Crear la aplicación FastAPI
app = FastAPI()

# Conexión a MongoDB
MONGO_URI = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo:27017/"
client = MongoClient(MONGO_URI)
db = client['mydatabase']
predictions_collection = db['predictions']

# Definir el esquema de entrada
class SizeInput(BaseModel):
    size: float

# Definir el modelo para la respuesta de la predicción
class PredictionResponse(BaseModel):
    id: str
    size: float
    predicted_price: float

# Definir el modelo para la respuesta de la lista de predicciones
class PredictionsResponse(BaseModel):
    id: str
    size: float
    predicted_price: float

# Definir el endpoint para predecir el precio
@app.post("/predict", response_model=PredictionResponse)
async def predict_price(input_data: SizeInput):
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

# Nuevo endpoint para obtener todas las predicciones
@app.get("/predictions", response_model=list[PredictionsResponse])
async def get_predictions():
    predictions = list(predictions_collection.find({}, {'_id': 0}))  # Obtener todos los documentos, sin el _id
    for prediction in predictions:
        prediction['id'] = str(prediction.get('id'))  # Asegurarse de que el id esté como string
    return predictions

# Endpoint de health check
@app.get('/health')
async def health_check():
    return {"status": "OK"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)