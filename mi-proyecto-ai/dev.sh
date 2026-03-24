#!/bin/bash

# Script para correr Docker Compose en modo desarrollo

echo "🐳 Iniciando proyecto con Docker Compose..."

# Verificar que docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚠️  Creando archivo .env..."
    cat > .env << EOF
# Backend
OPENAI_API_KEY=
GEMINI_API_KEY=
KIMI_API_KEY=
SECRET_KEY=your-secret-key-change-in-production
EOF
    echo "✅ Archivo .env creado - por favor agrega tus API keys"
fi

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose up

# Cleanup
echo "🛑 Limpiando..."
docker-compose down
