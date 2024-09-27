from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Cargar el modelo entrenado
model = joblib.load('src/model.pkl')

# Crear la aplicación FastAPI
app = FastAPI()

# Definir el esquema de entrada
class SizeInput(BaseModel):
    size: float

# Definir el endpoint para predecir el precio
@app.post("/predict")
def predict_price(input_data: SizeInput):
    size = input_data.size
    predicted_price = model.predict([[size]])[0]
    return {"size": size, "predicted_price": predicted_price}
