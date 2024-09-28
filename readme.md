Para proporcionar instrucciones claras en el archivo **README** para cualquier persona que clona tu repositorio, es importante cubrir desde los pasos de instalación de dependencias hasta cómo ejecutar correctamente la aplicación y los contenedores.

Aquí te dejo una guía completa que puedes incluir en tu **README.md**:

---

# Proyecto DevOps con Docker y FastAPI

Este proyecto incluye una aplicación **FastAPI** que realiza predicciones utilizando un modelo entrenado y un contenedor **Postgres** para gestionar la base de datos. Todo está orquestado con **Docker Compose**.

## Requisitos previos

Antes de ejecutar este proyecto, asegúrate de tener instalados los siguientes requisitos:

### 1. **Instalar Docker y Docker Compose**
   - Docker es necesario para ejecutar la aplicación dentro de contenedores.
   - Docker Compose es necesario para orquestar los múltiples contenedores (API y base de datos).

   Si no tienes Docker y Docker Compose instalados, puedes hacerlo siguiendo estos pasos:

   - **Instalar Docker**:
     - [Instrucciones para instalar Docker](https://docs.docker.com/get-docker/)
   
   - **Instalar Docker Compose**:
     - Docker Compose ya viene con Docker Desktop, pero si estás en Linux, puedes instalarlo con:
   
     ```bash
     sudo curl -L "https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```

### 2. **Clonar el repositorio**
   
   Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu_usuario/proyecto-devops.git
   cd proyecto-devops
   ```

## Instrucciones para ejecutar el proyecto

### 1. **Generar los datos iniciales**

   Antes de ejecutar la aplicación, es necesario generar el archivo CSV con los datos que utilizará el modelo. Puedes hacerlo ejecutando el siguiente script:

   ```bash
   python generate_data.py
   ```

   Esto creará el archivo `housing_data.csv` en la carpeta `data/`.

### 2. **Construir y ejecutar los contenedores con Docker Compose**

   Una vez que tengas Docker y Docker Compose instalados, puedes construir y levantar los contenedores con el siguiente comando:

   ```bash
   docker-compose up --build
   ```

   Esto construirá los contenedores (API y base de datos) y los iniciará.

   - La API estará disponible en `http://localhost:8000`.
   - El contenedor de Postgres estará corriendo en el puerto `5432`.

### 3. **Verificar la API**

   Una vez que los contenedores estén en ejecución, puedes verificar que la API esté funcionando correctamente accediendo a la documentación Swagger en:

   ```bash
   http://localhost:8000/docs
   ```

   Desde aquí, puedes probar los endpoints de la API, como el endpoint `/predict`.

### 4. **Apagar los contenedores**

   Cuando hayas terminado, puedes apagar los contenedores con el siguiente comando:

   ```bash
   docker-compose down
   ```

## Estructura del proyecto

```bash
📂 proyecto-devops
├── 📂 data                      # Carpeta donde se almacenan los datos CSV
├── 📂 docker                    # Contiene el Dockerfile para la API
├── 📂 src                       # Contiene el código fuente de la aplicación FastAPI y el modelo
│   ├── app.py                   # Aplicación FastAPI con un endpoint de predicción
│   └── model.pkl                # Archivo con el modelo entrenado
├── .github
│   └── 📂 workflows             # Contiene los archivos de CI/CD para GitHub Actions
│       ├── ci.yml               # Pipeline de CI para probar la construcción y la API
│       └── cd.yml               # Pipeline de CD para subir la imagen Docker a Docker Hub
├── docker-compose.yml           # Configuración de Docker Compose para levantar la API y la base de datos
├── Dockerfile                   # Archivo Docker para construir la imagen de la API
├── generate_data.py             # Script para generar el archivo de datos CSV
├── model.py                     # Script para entrenar el modelo de regresión
├── requirements.txt             # Lista de dependencias de Python
└── README.md                    # Instrucciones del proyecto
```

## Ejecutar pruebas locales de la API

Si prefieres ejecutar la API localmente sin Docker, sigue estos pasos:

### 1. **Instalar dependencias**

   Asegúrate de tener un entorno virtual para aislar las dependencias. Luego instala las dependencias desde `requirements.txt`:

   ```bash
   python -m venv devops_env
   source devops_env/bin/activate   # En Windows: devops_env\Scripts\activate
   pip install -r requirements.txt
   ```

### 2. **Ejecutar la API**

   Inicia la aplicación **FastAPI** localmente con el siguiente comando:

   ```bash
   uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
   ```

   La API estará disponible en `http://localhost:8000`.

### 3. **Entrenar el modelo (opcional)**

   Si deseas entrenar el modelo nuevamente, puedes ejecutar el script `model.py`:

   ```bash
   python model.py
   ```

   Esto guardará un nuevo archivo `model.pkl` en la carpeta `src/`.

## Contribuciones

Si deseas contribuir a este proyecto, sigue estos pasos:
1. Crea un **fork** del repositorio.
2. Crea una **branch** con tus cambios (`git checkout -b feature/nueva-feature`).
3. Haz **commit** de tus cambios (`git commit -m 'Agrego nueva feature'`).
4. Haz **push** a la branch (`git push origin feature/nueva-feature`).
5. Abre un **Pull Request**.

---

Con estas instrucciones, cualquier persona que clone el repositorio debería poder configurar su entorno, ejecutar la aplicación y probar la API, ya sea localmente o usando Docker.

¿Te gustaría agregar algo más o necesitas ajustar alguna sección?