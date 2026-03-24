# Project Structure Overview

Mi Proyecto AI está organizado en capas claramente definidas siguiendo patrones de arquitectura moderna.

## 📦 Stack Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer (Frontend)                      │
│  React + Vite + Axios                              │
├─────────────────────────────────────────────────────┤
│  API Layer (Backend)                                │
│  FastAPI Endpoints v1                              │
├─────────────────────────────────────────────────────┤
│  Business Logic Layer                               │
│  Services (Validators, Converters, Logic)          │
├─────────────────────────────────────────────────────┤
│  Integration Layer                                  │
│  GPT Client | Gemini Client | Kimi Client          │
├─────────────────────────────────────────────────────┤
│  Data Layer                                         │
│  SQLAlchemy ORM + PostgreSQL                        │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ Directorio Backend

```
backend/
├── app/
│   ├── __init__.py
│   │
│   ├── api/                           # 🛣️  Capa de Rutas
│   │   ├── __init__.py
│   │   ├── dependencies.py            # Inyección de dependencias
│   │   └── v1/                        # Versionado de API
│   │       ├── __init__.py
│   │       └── endpoints.py           # Endpoints de v1
│   │
│   ├── services/                      # 💼 Capa de Negocio
│   │   ├── __init__.py
│   │   ├── business_logic.py          # Lógica de negocio principal
│   │   ├── file_converter.py          # Conversión de archivos
│   │   └── validators.py              # Validaciones personalizadas
│   │
│   ├── integrations/                  # 🔌 Integraciones Externas
│   │   ├── __init__.py
│   │   ├── gpt_client.py              # OpenAI GPT
│   │   ├── gemini_client.py           # Google Gemini
│   │   └── kimi_client.py             # Moonshot Kimi
│   │
│   ├── models/                        # 📊 Modelos
│   │   ├── __init__.py
│   │   ├── db_models.py               # SQLAlchemy ORM
│   │   └── tensorflow_models/         # Modelos ML
│   │
│   ├── core/                          # ⚙️  Configuración Global
│   │   ├── __init__.py
│   │   ├── config.py                  # Settings y variables
│   │   └── security.py                # JWT y autenticación
│   │
│   └── db/                            # 🗄️  Base de Datos
│       ├── __init__.py
│       └── session.py                 # Conexión y sesiones
│
├── main.py                            # 🚀 Punto de entrada
├── requirements.txt                   # Dependencias
├── Dockerfile                         # Contenedorización
├── .env.example                       # Variables de ejemplo
└── .gitignore
```

### Propósito de cada carpeta:

**api/** - Define las rutas HTTP y controladores
- ✅ Validación de inputs
- ✅ Manejo de errores HTTP
- ✅ Respuestas formateadas

**services/** - Contiene la lógica de negocio
- ✅ Sin dependencias HTTP
- ✅ Reutilizable
- ✅ Testeable

**integrations/** - Clientes para APIs externas
- ✅ Pattern: Adapter/Gateway
- ✅ Manejo de errores específicos
- ✅ Configuración centralizada

**models/** - Modelos de dominio
- ✅ Esquemas SQLAlchemy
- ✅ Modelos ML
- ✅ Validaciones Pydantic

---

## ⚛️ Directorio Frontend

```
frontend/
├── src/
│   ├── components/                    # 🧩 Componentes Reutilizables
│   │   └── FileUploader.jsx           # Componente de carga
│   │
│   ├── pages/                         # 📄 Páginas/Vistas
│   │   └── Home.jsx                   # Página de inicio
│   │
│   ├── services/                      # 🔗 Servicios API
│   │   └── api.js                     # Cliente HTTP
│   │
│   ├── App.jsx                        # Componente raíz
│   ├── App.css                        # Estilos globales
│   └── main.jsx                       # Punto de entrada
│
├── public/                            # Archivos estáticos
├── index.html                         # HTML principal
├── package.json                       # Dependencias
├── vite.config.js                     # Configuración Vite
├── .env.example                       # Variables de ejemplo
└── .gitignore
```

### Propósito de cada carpeta:

**components/** - Componentes React reutilizables
- ✅ Props tipados
- ✅ Sin lógica de negocio
- ✅ Responsivos

**pages/** - Componentes de nivel superior (páginas)
- ✅ Manejo de rutas
- ✅ Lógica de página
- ✅ Integración de servicios

**services/** - Cliente HTTP y lógica de API
- ✅ Llamadas a backend
- ✅ Manejo de errores
- ✅ Interceptores

---

## 📚 Directorio docs/

```
docs/
├── ARCHITECTURE.md          # 📐 Descripción de arquitectura
├── API.md                   # 📡 Referencia de endpoints
├── DEPLOYMENT.md            # 🚀 Guía de despliegue
├── DEVELOPMENT.md           # 🛠️  Guía de desarrollo
├── DATABASE.md              # 🗄️  Esquema de BD
└── README.md                # 📖 Inicio rápido
```

---

## 🔄 Flujo de Datos

### Procesamiento de un Archivo

```
1. Frontend (React)
   └─► Carga archivo + selecciona modelo

2. API (FastAPI)
   └─► POST /api/v1/process-ai

3. Endpoint (endpoints.py)
   └─► Valida request + inyecta dependencias

4. Service (business_logic.py)
   └─► Selecciona modelo apropiado

5. Integration (gpt_client.py | gemini_client.py | kimi_client.py)
   └─► Llama API externa

6. Response
   └─► Retorna resultado al frontend
```

---

## 💾 Patrones de Diseño

### 1. Adapter Pattern (Integrations)
```python
# Todos los clientes implementan la misma interfaz
class GPTClient:
    async def process(self, content: str) -> dict

class GeminiClient:
    async def process(self, content: str) -> dict
```

### 2. Service Layer Pattern
```python
# BusinessLogic delega al cliente correcto
class BusinessLogic:
    async def process(self, content, model):
        if model == "gpt":
            return await self.gpt_client.process(content)
```

### 3. Repository Pattern
Preparado para futuras extensiones con ORM.

### 4. Factory Pattern
Posible en `BusinessLogic` para crear clientes.

---

## 🧪 Testing Structure

```
backend/tests/
├── test_api.py              # Tests de endpoints
├── test_services.py         # Tests de servicios
└── test_integrations.py     # Tests de integraciones

frontend/src/__tests__/
├── components.test.jsx      # Tests de componentes
└── services.test.js         # Tests de servicios
```

---

## 📊 Dependencias Clave

### Backend
```
FastAPI         ← Framework web
Uvicorn         ← ASGI server
Pydantic        ← Validación
SQLAlchemy      ← ORM
PostgreSQL      ← Database
TensorFlow      ← ML
OpenAI          ← API integración
google-generativeai ← API integración
```

### Frontend
```
React           ← Framework UI
Vite            ← Build tool
Axios           ← HTTP client
```

---

## 🔐 Seguridad

- **JWT** en core/security.py
- **CORS** configurado en main.py
- **Variables de entorno** en .env
- **Validación** en services/validators.py

---

## 📈 Escalabilidad

El proyecto está diseñado para:
- ✅ Agregar nuevos clientes AI
- ✅ Agregar nuevos tipos de archivos
- ✅ Versionar API (v2, v3, etc.)
- ✅ Cambiar BD sin afectar API
- ✅ Agregar autenticación avanzada

---

## 🔗 Referencias

- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev
- PostgreSQL: https://www.postgresql.org/docs
- Vite: https://vitejs.dev
- SQLAlchemy: https://docs.sqlalchemy.org
