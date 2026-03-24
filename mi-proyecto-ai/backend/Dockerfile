# Etapa de construcción
FROM python:3.11-slim as builder

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa final
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /root/.local /root/.local

# Copiar código de la aplicación
COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["python", "main.py"]
