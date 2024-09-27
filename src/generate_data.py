import os
import pandas as pd

# Crear los datos
data = {
    'size': [750, 800, 850, 900, 950, 1000, 1100, 1200],
    'price': [150000, 170000, 180000, 200000, 210000, 230000, 250000, 270000]
}

# Crear un DataFrame de pandas
df = pd.DataFrame(data)

# Crear la carpeta 'data' si no existe
os.makedirs('data', exist_ok=True)

# Guardar el CSV en la carpeta 'data'
df.to_csv('data/housing_data.csv', index=False)

print("Archivo CSV 'housing_data.csv' generado en la carpeta 'data'.")
