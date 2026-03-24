# README - Mi Proyecto AI

<div align="center">
  <h1>🤖 Mi Proyecto AI</h1>
  <p>Plataforma de procesamiento con múltiples modelos de inteligencia artificial</p>
  
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
  [![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react)](https://react.dev)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://www.postgresql.org)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

---

## 🌟 Características

✅ **Múltiples Modelos de IA**
- OpenAI GPT-4
- Google Gemini
- Moonshot Kimi

✅ **Soporte de Archivos**
- Texto (.txt)
- PDF (.pdf)
- CSV (.csv)
- DOCX (.docx)

✅ **Arquitectura Escalable**
- Backend en FastAPI
- Frontend en React + Vite
- Database PostgreSQL

✅ **Fácil Despliegue**
- Railway (Backend)
- Vercel (Frontend)

✅ **API RESTful**
- Documentación automática con Swagger
- Autenticación JWT
- Rate limiting

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Ejecutar
python main.py
```

API disponible en: http://localhost:8000

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

App disponible en: http://localhost:3000

---

## 📚 Documentación

Para documentación detallada, consulta:

- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Descripción de la arquitectura
- **[API.md](./docs/API.md)** - Referencia de endpoints
- **[DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Guía de despliegue
- **[DEVELOPMENT.md](./docs/DEVELOPMENT.md)** - Guía de desarrollo
- **[DATABASE.md](./docs/DATABASE.md)** - Esquema de BD

---

## 🏗️ Estructura del Proyecto

```
mi-proyecto-ai/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints
│   │   ├── services/          # Lógica de negocio
│   │   ├── integrations/      # Clientes de IA
│   │   ├── models/            # Modelos DB y ML
│   │   ├── core/              # Configuración
│   │   └── db/                # Base de datos
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # App React
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
└── docs/                       # Documentación
    ├── ARCHITECTURE.md
    ├── API.md
    ├── DEPLOYMENT.md
    ├── DEVELOPMENT.md
    └── DATABASE.md
```

---

## 📡 API Endpoints

```http
# Health check
GET /health
Response: { "status": "ok" }

# Procesar con IA
POST /api/v1/process-ai
Content-Type: multipart/form-data
- file: Binary
- model: "gpt" | "gemini" | "kimi"

# Modelos disponibles
GET /api/v1/models
Response: { "models": [...] }
```

Ver [API.md](./docs/API.md) para documentación completa.

---

## 🔐 Configuración de Variables de Entorno

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/db_name
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
KIMI_API_KEY=...
SECRET_KEY=your-secret-key
DEBUG=False
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

---

## 🚢 Despliegue en Producción

### Backend - Railway

1. Conectar repositorio en Railway
2. Configurar variables de entorno
3. Railway detectará Dockerfile
4. Deploy automático

URL: `https://mi-proyecto-ai-prod.railway.app`

### Frontend - Vercel

1. Importar proyecto en Vercel
2. Configurar `VITE_API_URL`
3. Deploy automático

URL: `https://mi-proyecto-ai.vercel.app`

Ver [DEPLOYMENT.md](./docs/DEPLOYMENT.md) para instrucciones detalladas.

---

## 🛠️ Desarrollo

### Ejecutar Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

### Linting

```bash
# Backend
black app/
flake8 app/

# Frontend
npm run lint
```

### Build para Producción

```bash
# Backend (Docker)
docker build -t mi-proyecto-ai .

# Frontend
npm run build
```

---

## 📖 Ejemplos de Uso

### Procesar Archivo con JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/v1/process-ai', {
  method: 'POST',
  body: formData,  // archivo + modelo
});
const result = await response.json();
console.log(result.result.response);
```

### Procesar Archivo con Python

```python
import requests

files = {'file': open('document.txt', 'rb')}
data = {'model': 'gpt'}
response = requests.post(
  'http://localhost:8000/api/v1/process-ai',
  files=files,
  data=data
)
print(response.json())
```

Ver [API.md](./docs/API.md) para más ejemplos.

---

## 🐛 Troubleshooting

### Error: "Could not connect to database"
```bash
# Verificar PostgreSQL está ejecutando
psql -U postgres  # Debería conectar

# Verificar DATABASE_URL en .env
```

### Error: "Port already in use"
```bash
# Cambiar puerto o matar proceso
# Backend: uvicorn main:app --port 8001
# Frontend: npm run dev -- --port 3001
```

### Error: "API Key invalid"
- Regenerar keys en consolas de proveedores
- Actualizar .env
- Reiniciar servidor

Ver [DEVELOPMENT.md](./docs/DEVELOPMENT.md) para más troubleshooting.

---

## 📊 Stack Tecnológico

**Backend**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL 15
- TensorFlow 2.15.0

**Frontend**
- React 18.2.0
- Vite 5.0.0
- Axios 1.6.0

**DevOps**
- Docker
- Railway
- Vercel

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📞 Contacto

- Email: dumar22@example.com
- GitHub: [@Dumar22](https://github.com/Dumar22)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos

- FastAPI por el increíble framework
- React por la librería de UI
- PostgreSQL por la base de datos
- OpenAI, Google y Moonshot por las APIs de IA

---

## 🎯 Roadmap

- [ ] Agregar autenticación con Google/GitHub
- [ ] Panel de administración
- [ ] Historial de procesamientos
- [ ] Exportar resultados (PDF, Excel)
- [ ] Soporte para más modelos de IA
- [ ] Apps móviles (iOS/Android)
- [ ] Análisis de costos
- [ ] Rate limiting avanzado

---

**Made with ❤️ by [Dumar22](https://github.com/Dumar22)**
