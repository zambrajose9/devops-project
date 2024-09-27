import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Cargar datos desde el CSV
def load_data():
    data_path = 'data/housing_data.csv'
    data = pd.read_csv(data_path)
    return data

# Entrenar el modelo de regresión lineal
def train_model(data):
    X = data[['size']]  # Variables independientes
    y = data['price']   # Variable dependiente
    model = LinearRegression()
    model.fit(X, y)
    return model

# Guardar el modelo entrenado en un archivo .pkl
def save_model(model):
    model_path = 'src/model.pkl'
    joblib.dump(model, model_path)
    print(f'Modelo entrenado y guardado en {model_path}')

# Crear la carpeta 'src' si no existe
os.makedirs('src', exist_ok=True)

# Proceso completo
if __name__ == '__main__':
    data = load_data()
    model = train_model(data)
    save_model(model)
