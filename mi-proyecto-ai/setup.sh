#!/bin/bash

# Script para inicializar el proyecto localmente

echo "🚀 Inicializando Mi Proyecto AI..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend
echo -e "${YELLOW}📦 Configurando Backend...${NC}"

cd backend

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -q -r requirements.txt

# Configurar .env
if [ ! -f ".env" ]; then
    echo "Copiando .env.example a .env..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Por favor configura .env con tus credenciales${NC}"
fi

cd ..

# Frontend
echo -e "${YELLOW}📦 Configurando Frontend...${NC}"

cd frontend

# Instalar dependencias
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias..."
    npm install -q
fi

# Configurar .env
if [ ! -f ".env" ]; then
    echo "Copiando .env.example a .env..."
    cp .env.example .env
fi

cd ..

echo -e "${GREEN}✅ Inicialización completada!${NC}"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo "1. Backend: cd backend && source venv/bin/activate && python main.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo -e "${YELLOW}O usa Docker:${NC}"
echo "docker-compose up"
