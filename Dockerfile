# Imagen base de Python
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y activar salida sin buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Carpeta de trabajo
WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL y compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para arrancar el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
