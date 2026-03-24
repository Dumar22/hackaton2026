# Quick Start Guide

## 🚀 Inicio Rápido (5 minutos)

### Opción 1: Docker Compose (Recomendado)

```bash
# 1. Ir a la carpeta del proyecto
cd mi-proyecto-ai

# 2. Hacer el script ejecutable
chmod +x dev.sh

# 3. Ejecutar
./dev.sh
```

**URLs**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Database: localhost:5432

---

### Opción 2: Setup Manual

#### Backend

```bash
# 1. Abrir terminal 1
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env

# 2. Asegurar PostgreSQL esté corriendo
psql -U postgres  # Debería conectar

# 3. Ejecutar
python main.py
```

#### Frontend

```bash
# 1. Abrir terminal 2
cd frontend
npm install
cp .env.example .env

# 2. Ejecutar
npm run dev
```

---

## 🧪 Verificar que funciona

```bash
# Health check
curl http://localhost:8000/health

# Debería responder:
# {"status": "ok"}

# Ver Swagger UI
# Abre en el navegador: http://localhost:8000/docs
```

---

## 📁 Estructura

```
mi-proyecto-ai/
├── backend/          # API FastAPI
├── frontend/         # App React
├── docs/             # Documentación
├── docker-compose.yml
├── setup.sh
├── dev.sh
└── README.md
```

---

## 📚 Documentación

- **[README.md](./README.md)** - Visión general
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Arquitectura
- **[docs/API.md](./docs/API.md)** - Endpoints
- **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Despliegue
- **[docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Desarrollo
- **[docs/DATABASE.md](./docs/DATABASE.md)** - Base de datos

---

## 🔧 Configuración

### Backend (.env)

```env
DATABASE_URL=postgresql://ai_user:password123@localhost:5432/ai_project_db
OPENAI_API_KEY=sk-...    # Obtener en platform.openai.com
GEMINI_API_KEY=...       # Obtener en makersuite.google.com
KIMI_API_KEY=...         # Obtener en kimi.ai
SECRET_KEY=your-secret
DEBUG=False
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## 🚀 Próximos Pasos

1. ✅ Clonar/descargar el proyecto
2. ✅ Configurar variables de entorno
3. ✅ Iniciar con Docker o manualmente
4. ✅ Acceder a http://localhost:3000
5. ✅ Revisar documentación en `docs/`

---

## 💡 Tips

- Usar `npm run dev` para hot reload en frontend
- Ver logs en tiempo real durante desarrollo
- Usar Swagger UI para probar API endpoints
- Revisar `DEVELOPMENT.md` para guía detallada

---

## 🆘 Problemas?

1. Verificar que PostgreSQL está running
2. Verificar que ports 3000, 8000, 5432 están disponibles
3. Revisar `docs/DEVELOPMENT.md` - Troubleshooting
4. Verificar logs en terminal

---

**¡Listo para desarrollar! 🎉**

Para más información, consulta la documentación detallada en `docs/`.
