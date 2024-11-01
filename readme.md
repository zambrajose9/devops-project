```markdown
# Proyecto de Predicción de Precios de Casas

Este proyecto implementa una API para predecir el precio de una casa en función de su tamaño utilizando un modelo de regresión. La API está construida con FastAPI, y el proyecto incluye un pipeline de CI/CD, monitoreo con Prometheus y visualización de métricas en Grafana. La persistencia de datos se maneja con MongoDB.

## Estructura del Proyecto

```
devops/
├── .github/
│   └── workflows/
│       ├── ci.yml                # Pipeline de Integración Continua
│       └── cd.yml                # Pipeline de Despliegue Continuo
├── data/
│   └── housing_data.csv          # Datos de ejemplo
├── docker/
│   └── Dockerfile                # Archivo Docker para construir la imagen de la app
├── prometheus/
│   └── prometheus.yml            # Configuración para Prometheus
├── src/
│   ├── __pycache__/
│   ├── app.py                    # Archivo principal de la aplicación FastAPI
│   ├── model.pkl                 # Modelo de regresión entrenado
│   └── model.py                  # Código para entrenar el modelo
├── tests/
│   └── test_main.py              # Pruebas unitarias de la API
├── .gitignore                    # Archivos a ignorar por Git
├── docker-compose.yml            # Archivo de configuración para Docker Compose
├── LICENSE                       # Licencia del proyecto
├── README_dev.md                 # Documentación adicional para desarrollo
└── requirements.txt              # Dependencias del proyecto
```

## Requisitos Previos

- **Docker**: Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
- **GitHub Secrets**: Configura los secretos necesarios en GitHub para que los pipelines CI/CD funcionen correctamente.

## Instrucciones de Instalación y Ejecución

### 1. Clonar el Repositorio

Clona el repositorio a tu máquina local:

```bash
git clone https://github.com/tu-usuario/devops-project.git
cd devops-project
```

### 2. Configuración del Entorno

El proyecto usa Docker Compose para orquestar los servicios. Asegúrate de tener Docker en ejecución y de que los puertos 8000, 27017, 9090 y 3000 estén libres en tu sistema.

### 3. Archivos de Configuración Importantes

#### docker-compose.yml

Este archivo define y configura los servicios:

- **app**: La aplicación FastAPI con el modelo de predicción.
- **mongo**: Base de datos MongoDB para almacenar predicciones.
- **prometheus**: Herramienta de monitoreo para recolectar métricas.
- **grafana**: Visualizador de métricas.

#### prometheus.yml

Configura Prometheus para recolectar métricas de la API.

```yaml
scrape_configs:
  - job_name: 'fastapi'
    scrape_interval: 5s
    metrics_path: /metrics
    static_configs:
      - targets: ['app:8000']
```

### 4. Construir y Ejecutar los Servicios

Construye y ejecuta los servicios definidos en `docker-compose.yml`:

```bash
docker-compose up --build -d
```

Esto ejecutará los siguientes servicios:

- **FastAPI** en `http://localhost:8000`
- **MongoDB** en el puerto 27017
- **Prometheus** en `http://localhost:9090`
- **Grafana** en `http://localhost:3000` (contraseña de administrador configurada en el archivo docker-compose)

### 5. Verificación de la API

Puedes verificar que la API esté en funcionamiento visitando la documentación interactiva generada automáticamente por FastAPI:

```
http://localhost:8000/docs
```

### 6. Monitoreo con Prometheus y Grafana

#### Prometheus

Prometheus estará recolectando métricas desde la API. Puedes acceder a la interfaz de Prometheus en:

```
http://localhost:9090
```

#### Grafana

Para visualizar las métricas, ingresa a Grafana en:

```
http://localhost:3000
```

Inicia sesión (la contraseña está configurada en `docker-compose.yml`) y añade Prometheus como fuente de datos para crear paneles de métricas personalizados.

### 7. Ejecución de Pruebas Unitarias

Las pruebas unitarias están definidas en `tests/test_main.py` y se ejecutan en el contenedor de la aplicación usando `pytest`.

Ejecuta las pruebas con:

```bash
docker-compose exec app python -m pytest
```

### Pipelines de CI/CD

Los workflows de CI/CD están definidos en los archivos `.github/workflows/ci.yml` y `.github/workflows/cd.yml`.

#### CI (Integración Continua)

El pipeline de CI (`ci.yml`) se ejecuta en cada push y pull request a la rama `main`. Incluye los siguientes pasos:

1. Descarga el repositorio.
2. Configura Docker Buildx.
3. Instala Docker Compose.
4. Construye y ejecuta los servicios.
5. Verifica que la API esté funcionando.
6. Ejecuta pruebas unitarias.
7. Apaga y elimina los contenedores.

#### CD (Despliegue Continuo)

El pipeline de CD (`cd.yml`) sigue pasos similares al CI pero incluye la configuración de servicios adicionales como MongoDB, Prometheus y Grafana, asegurando que la aplicación se despliegue correctamente en un entorno de producción.

### Descripción Detallada de Archivos Clave

- **`Dockerfile`**: Configura el contenedor de la aplicación, separando la instalación de dependencias y la ejecución del código en diferentes etapas.
- **`app.py`**: Implementa la lógica de la API FastAPI, incluyendo los endpoints `/predict` para realizar predicciones y `/metrics` para exponer métricas personalizadas a Prometheus.
- **`test_main.py`**: Contiene pruebas unitarias que verifican el correcto funcionamiento de la API.
- **`prometheus.yml`**: Configura Prometheus para que recolecte métricas de la aplicación cada 5 segundos.

### Ejemplo de Uso

1. Realiza una predicción enviando una solicitud `POST` a `/predict` con el tamaño de la casa en el cuerpo de la solicitud.
2. Consulta todas las predicciones almacenadas con una solicitud `GET` a `/predictions`.

---
