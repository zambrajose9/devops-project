# Notas para el desarrollo pendiente

Este documento describe los aspectos pendientes del proyecto y las tareas adicionales que se deben completar para que el proyecto esté finalizado de acuerdo con los requerimientos del trabajo práctico.

## Tareas pendientes

### 1. **Monitoreo y logging**

Actualmente, el proyecto no tiene herramientas de monitoreo o logging implementadas. Para completarlo, es necesario:

- **Monitoreo**: Integrar herramientas como **Prometheus** y **Grafana** para monitorear la aplicación y el contenedor de base de datos. Alternativamente, utilizar alguna solución de monitoreo sencilla basada en métricas de Docker o FastAPI.
- **Logging**: Asegurarse de que los logs de la API (FastAPI) y los contenedores se estén capturando y almacenando correctamente. Esto puede incluir habilitar logs detallados para la aplicación y capturarlos desde Docker.

#### Recursos útiles:
- [Documentación de Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Documentación de FastAPI logging](https://fastapi.tiangolo.com/advanced/custom-loggers/)

---

### 2. **Pruebas unitarias**

No se han implementado pruebas unitarias o funcionales para verificar el correcto funcionamiento de la API.

- Implementar pruebas usando **pytest** para verificar los endpoints clave de la API, como `/predict`.
- Incluir las pruebas en la pipeline de CI (`ci.yml`) para que se ejecuten automáticamente cada vez que se realice un `push`.

#### Recursos útiles:
- [pytest](https://docs.pytest.org/en/stable/)

---

### 3. **Revisión de la documentación (README.md)**

El archivo principal `README.md` ya incluye una guía general para ejecutar el proyecto. Sin embargo, se debe realizar una revisión final para asegurarse de que:

- Todos los pasos de instalación y ejecución estén claros.
- Se incluyan ejemplos de uso de la API (por ejemplo, cómo hacer una petición a `/predict`).
- Incluir una sección que explique el uso de Docker Compose y cómo se interconectan los servicios.

---

## Otras sugerencias

### 1. **Optimización de contenedores**

Podrías investigar si la imagen Docker de la API puede ser optimizada para reducir su tamaño. Algunos pasos para esto podrían incluir:

- Utilizar imágenes base más ligeras, como `python:3.10-alpine`.
- Aplicar técnicas de multi-stage build en el `Dockerfile` para reducir el tamaño final de la imagen.

---

## Referencias adicionales

Si necesitas más información sobre Docker, Docker Compose, FastAPI o Prometheus, estos recursos te serán de ayuda:

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Documentación oficial de Docker Compose](https://docs.docker.com/compose/)
- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación oficial de Prometheus](https://prometheus.io/docs/introduction/overview/)

---

## Última actualización
Esta guía fue actualizada por última vez el **[28/09/2024]**.
