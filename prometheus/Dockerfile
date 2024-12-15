FROM prom/prometheus:latest

# Copiar el archivo de configuración de Prometheus
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Comando para iniciar Prometheus
CMD ["--config.file=/etc/prometheus/prometheus.yml"]
