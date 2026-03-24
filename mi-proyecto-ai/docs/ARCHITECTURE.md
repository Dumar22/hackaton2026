# Documentación de Arquitectura - Mi Proyecto AI

## 📋 Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Arquitectura](#arquitectura)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura de Carpetas](#estructura-de-carpetas)
5. [Instalación](#instalación)
6. [Despliegue](#despliegue)
7. [API Endpoints](#api-endpoints)
8. [Integración con IA](#integración-con-ia)

## 🎯 Visión General

Mi Proyecto AI es una plataforma escalable que integra múltiples modelos de inteligencia artificial (GPT, Gemini, Kimi) con un backend robusto y un frontend interactivo.

### Características Principales
- ✅ Soporte para múltiples modelos de IA
- ✅ Procesamiento de archivos (TXT, PDF, CSV, DOCX)
- ✅ Validación y conversión de archivos
- ✅ API RESTful con autenticación JWT
- ✅ Base de datos relacional (PostgreSQL)
- ✅ Despliegue en Railway (Backend) y Vercel (Frontend)

---

## 🏗️ Arquitectura

```
┌─────────────────┐         ┌──────────────────┐
│   Frontend      │         │   Backend        │
│  (React/Vite)   │◄───────►│  (FastAPI)       │
│   Vercel        │ HTTP    │  Railway         │
└─────────────────┘         └──────────────────┘
                                    │
                                    ├─► GPT
                                    ├─► Gemini
                                    ├─► Kimi
                                    │
                                    ▼
                            ┌──────────────────┐
                            │   PostgreSQL     │
                            │   Database       │
                            └──────────────────┘
```

### Patrones de Diseño Utilizados

#### 1. **Gateway Pattern** (Clientes de IA)
- Encapsula la comunicación con diferentes APIs de IA
- Facilita el cambio entre proveedores
- Manejo centralizado de errores

#### 2. **Adapter Pattern** (Conversión de Archivos)
- Adapta diferentes formatos de archivo a un formato común
- Extensible para nuevos formatos

#### 3. **Service Layer Pattern**
- Separación clara entre lógica de negocio y API
- Facilita testing y mantenimiento

#### 4. **Repository Pattern**
- Abstracción de la capa de datos
- Facilita cambios futuros en la BD

---

## 💻 Stack Tecnológico

### Backend
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework | FastAPI | 0.104.1 |
| Server | Uvicorn | 0.24.0 |
| Validación | Pydantic | 2.5.0 |
| ORM | SQLAlchemy | 2.0.23 |
| BD | PostgreSQL | 15+ |
| ML | TensorFlow | 2.15.0 |
| APIs | aiohttp | 3.9.1 |
| Auth | JWT | HS256 |

### Frontend
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework | React | 18.2.0 |
| Build Tool | Vite | 5.0.0 |
| HTTP Client | Axios | 1.6.0 |
| Styling | CSS3 | - |

---

## 📁 Estructura de Carpetas

```
mi-proyecto-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   └── endpoints.py (Rutas de la API)
│   │   │   └── dependencies.py (Inyección de dependencias)
│   │   │
│   │   ├── services/
│   │   │   ├── business_logic.py (Lógica de negocio)
│   │   │   ├── file_converter.py (Conversión de archivos)
│   │   │   └── validators.py (Validaciones)
│   │   │
│   │   ├── integrations/
│   │   │   ├── gpt_client.py (Cliente OpenAI)
│   │   │   ├── gemini_client.py (Cliente Google Gemini)
│   │   │   └── kimi_client.py (Cliente Kimi AI)
│   │   │
│   │   ├── models/
│   │   │   ├── db_models.py (Modelos de BD)
│   │   │   └── tensorflow_models/ (Modelos ML)
│   │   │
│   │   ├── core/
│   │   │   ├── config.py (Configuración global)
│   │   │   └── security.py (Autenticación/Autorización)
│   │   │
│   │   └── db/
│   │       └── session.py (Conexión a BD)
│   │
│   ├── main.py (Punto de entrada)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── FileUploader.jsx
│   │   ├── services/
│   │   │   └── api.js (Cliente API)
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── App.jsx (Componente raíz)
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── .env.example
│
└── docs/
    ├── ARCHITECTURE.md (Este archivo)
    ├── API.md
    ├── DEPLOYMENT.md
    ├── DEVELOPMENT.md
    └── DATABASE.md
```

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

### Backend

```bash
# 1. Navegar a la carpeta del backend
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 6. Ejecutar la aplicación
python main.py
```

La API estará disponible en: `http://localhost:8000`

### Frontend

```bash
# 1. Navegar a la carpeta del frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Ejecutar en modo desarrollo
npm run dev
```

La aplicación estará disponible en: `http://localhost:3000`

---

## 🌐 Despliegue

### Backend - Railway

1. **Signup en Railway**: https://railway.app

2. **Conectar repositorio**:
   - Autorizar GitHub
   - Seleccionar repositorio

3. **Configurar variables de entorno** en Railway:
   ```
   DATABASE_URL=postgresql://...
   OPENAI_API_KEY=sk-...
   GEMINI_API_KEY=...
   KIMI_API_KEY=...
   SECRET_KEY=...
   ```

4. **Deploy**:
   - Railway detectará automáticamente `Dockerfile`
   - Hará build y deploy

### Frontend - Vercel

1. **Signup en Vercel**: https://vercel.com

2. **Importar proyecto**:
   - Conectar con GitHub
   - Seleccionar repositorio

3. **Configurar variables de entorno**:
   ```
   VITE_API_URL=https://mi-proyecto-ai-prod.railway.app
   ```

4. **Deploy**:
   - Vercel construirá automáticamente
   - Disponible en: `https://tu-proyecto.vercel.app`

---

## 📡 API Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

### Procesar con IA
```http
POST /api/v1/process-ai
Content-Type: multipart/form-data

file: <binary>
model: "gpt" | "gemini" | "kimi"
```

Response:
```json
{
  "success": true,
  "result": {
    "model": "gpt-4",
    "response": "...",
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 20,
      "total_tokens": 30
    }
  }
}
```

### Obtener Modelos Disponibles
```http
GET /api/v1/models
```

Response:
```json
{
  "models": ["gpt", "gemini", "kimi"],
  "description": "Modelos de IA disponibles"
}
```

---

## 🤖 Integración con IA

### GPT (OpenAI)

```python
from app.integrations.gpt_client import GPTClient

client = GPTClient()
result = await client.process("Tu contenido aquí")
```

**Requisitos**:
- API Key de OpenAI
- Modelo: gpt-4

### Gemini (Google)

```python
from app.integrations.gemini_client import GeminiClient

client = GeminiClient()
result = await client.process("Tu contenido aquí")
```

**Requisitos**:
- API Key de Google Gemini
- Modelo: gemini-pro

### Kimi (Moonshot)

```python
from app.integrations.kimi_client import KimiClient

client = KimiClient()
result = await client.process("Tu contenido aquí")
```

**Requisitos**:
- API Key de Kimi
- Endpoint: api.kimi.ai

---

## 🔐 Seguridad

### Autenticación (JWT)
- Tokens con expiración configurables
- Validación en cada request
- Refresh token support

### Validaciones
- Size limit de archivos: 50MB
- Tipos de archivo permitidos
- Sanitización de inputs
- CORS configurado

### Variables de Entorno
Nunca commitear `.env` - usar `.env.example` como template

---

## 📝 Notas Importantes

1. **Base de Datos**: Asegurar conexión a PostgreSQL antes de iniciar
2. **API Keys**: Nunca compartir ni commitear en Git
3. **Rate Limiting**: Implementar en producción
4. **Logging**: Configurable por nivel (DEBUG, INFO, WARNING, ERROR)
5. **Testing**: Agregar tests unitarios y de integración

---

## 📞 Soporte

Para más información, consultar los archivos de documentación complementaria:
- [API.md](./API.md) - Referencia completa de endpoints
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía de despliegue
- [DATABASE.md](./DATABASE.md) - Esquema de BD
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Guía de desarrollo
