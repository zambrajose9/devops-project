# Usa la imagen oficial de Grafana
FROM grafana/grafana:latest

# Expone el puerto 3000 (puerto predeterminado de Grafana)
EXPOSE 3000

# Configuración de entorno opcional (puedes agregar más si es necesario)
ENV GF_SECURITY_ADMIN_USER=admin
ENV GF_SECURITY_ADMIN_PASSWORD=admin123

# Comando para iniciar Grafana
CMD ["/run.sh"]
