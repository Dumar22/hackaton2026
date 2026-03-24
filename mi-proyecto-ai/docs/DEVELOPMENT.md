# Guía de Desarrollo - Mi Proyecto AI

## 🎯 Objetivo de esta Guía

Ayudarte a configurar tu entorno de desarrollo local para trabajar en el proyecto de forma eficiente.

---

## 📦 Configuración Inicial

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Dumar22/hackaton2026.git
cd hackaton2026/mi-proyecto-ai
```

### 2. Estructura del Workspace

```bash
# VS Code - Recommended
code .

# O abrir en tu editor favorito
```

---

## 🔧 Backend Setup

### Entorno Virtual Python

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv

# Activar según tu SO:
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Instalar Dependencias

```bash
# Instalar requirements
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install pytest pytest-cov black flake8 mypy
```

### Configurar Variables de Entorno

```bash
# Copiar archivo ejemplo
cp .env.example .env

# Editar .env con tus valores
# DATABASE_URL (local PostgreSQL)
# API Keys de los servicios
```

### Ejecutar Backend

```bash
# Desarrollo (con reload automático)
python main.py

# O usar uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Acceder a**:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ⚛️ Frontend Setup

### Node.js

```bash
cd frontend

# Verificar versión (debe ser 18+)
node --version
npm --version
```

### Instalar Dependencias

```bash
npm install
```

### Configurar Variables de Entorno

```bash
# Copiar archivo ejemplo
cp .env.example .env

# Por defecto ya viene configurado para localhost
# VITE_API_URL=http://localhost:8000
```

### Ejecutar Frontend

```bash
# Modo desarrollo con HMR
npm run dev

# Construir para producción
npm run build

# Previsualizar build
npm run preview
```

**Acceder a**: http://localhost:3000

---

## 🗄️ Base de Datos

### Instalar PostgreSQL (si no lo tienes)

**macOS**:
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows**:
- Descargar desde: https://www.postgresql.org/download/windows/

### Crear Base de Datos Local

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE ai_project_db;

# Crear usuario
CREATE USER ai_user WITH PASSWORD 'password123';
ALTER ROLE ai_user SET client_encoding TO 'utf8';
ALTER ROLE ai_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE ai_project_db TO ai_user;

# Salir
\q
```

### Actualizar .env

```env
DATABASE_URL=postgresql://ai_user:password123@localhost:5432/ai_project_db
```

### Crear Tablas

```bash
# Desde la carpeta backend
python -c "from app.models.db_models import Base; from app.db.session import engine; Base.metadata.create_all(bind=engine)"
```

---

## 📝 Estructura de Código

### Backend - Naming Conventions

```python
# Clases: PascalCase
class UserService:
    pass

# Funciones/Métodos: snake_case
async def process_file():
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 50 * 1024 * 1024

# Privadas: _leading_underscore
_internal_helper = None
```

### Frontend - Naming Conventions

```javascript
// Componentes: PascalCase
const FileUploader = () => {}

// Funciones: camelCase
const processData = () => {}

// Constantes: UPPER_SNAKE_CASE o camelCase
const MAX_SIZE = 50 * 1024 * 1024
const apiUrl = 'http://localhost:8000'
```

---

## ✅ Tests

### Backend - Pytest

```bash
cd backend

# Instalar pytest
pip install pytest pytest-cov

# Crear archivo de test
# tests/test_api.py

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_api.py::test_health_check -v
```

**Estructura de Tests**:
```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_services.py
│   └── test_integrations.py
```

### Frontend - Vitest

```bash
cd frontend

# Instalar vitest
npm install -D vitest

# Ejecutar tests
npm run test
```

---

## 🎨 Code Quality

### Backend

**Black** (Formatear código):
```bash
black app/
```

**Flake8** (Linter):
```bash
flake8 app/
```

**MyPy** (Type checking):
```bash
mypy app/
```

**Pre-commit Hook**:
```bash
# Instalar
pip install pre-commit

# Configurar (.pre-commit-config.yaml)
# Ejecutar antes de cada commit
pre-commit run --all-files
```

### Frontend

**ESLint**:
```bash
npm run lint
```

**Prettier** (Formatter):
```bash
npm install -D prettier
npx prettier --write src/
```

---

## 🐛 Debugging

### Backend - VS Code

Crear `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

### Frontend - VS Code

Extensión: **Debugger for Chrome/Edge**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch React Dev",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src",
      "sourceMapPathOverride": {}
    }
  ]
}
```

---

## 📚 Extensiones VS Code Recomendadas

### Backend
- Python
- Pylance
- Python Docstring Generator
- SQLTools

### Frontend
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- ESLint
- Thunder Client (para API testing)

### Ambos
- Git Graph
- Thunder Client
- REST Client
- Markdown Preview Enhanced

---

## 🔄 Git Workflow

### Feature Branching

```bash
# Crear rama para feature
git checkout -b feature/nombre-feature

# Hacer cambios
git add .
git commit -m "feat: descripción breve"

# Push
git push origin feature/nombre-feature

# Pull Request en GitHub
```

### Commit Messages

```
feat: agregar nueva funcionalidad
fix: corregir bug
docs: actualizar documentación
style: cambios de formato
refactor: refactorizar código
test: agregar tests
chore: mantenimiento
```

---

## 🚀 Workflow Recomendado para Desarrollo

### Inicio del día

```bash
# Actualizar código
git pull origin main

# Backend
cd backend
source venv/bin/activate
python main.py

# En otra terminal - Frontend
cd frontend
npm run dev

# En otra terminal - Database
# Verificar que PostgreSQL esté running
```

### Durante el desarrollo

```bash
# Cambios frecuentes - los servidores recargan automáticamente

# Ejecutar tests antes de commit
pytest
npm run lint

# Commit
git add .
git commit -m "feat: descripción"
git push
```

### Fin del día

```bash
# Asegurar que todo esté commiteado
git status

# Push final
git push origin nombre-rama
```

---

## 📋 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### Error: "Could not connect to database"
- Verificar PostgreSQL está running
- Verificar `DATABASE_URL` en `.env`
- Crear database si no existe

### Error: "Port 8000 already in use"
```bash
# Linux/Mac: Encontrar y matar proceso
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "npm ERR! ERESOLVE unable to resolve dependency tree"
```bash
npm install --legacy-peer-deps
```

---

## 🎓 Recursos de Aprendizaje

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **PostgreSQL**: https://www.postgresql.org/docs
- **Vite**: https://vitejs.dev
- **Git**: https://git-scm.com/doc

---

## 💡 Tips and Tricks

### Backend
- Usar `debugger` breakpoints en VS Code
- Acceder a `/docs` para Swagger UI
- Usar `print()` para debugging rápido
- Verificar logs en consola

### Frontend
- Usar React DevTools extension
- Usar Redux DevTools para estado
- Usar Network tab en DevTools
- Hot reload automático con Vite

---

## ✨ Siguientes Pasos

1. Familiarizarse con la estructura
2. Revisar documentación de API
3. Crear una rama para empezar a trabajar
4. Hacer un pequeño cambio y verificar que funciona
5. Crear tu primer Pull Request
