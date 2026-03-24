# Guía de Despliegue - Mi Proyecto AI

## 📋 Pre-requisitos

- Cuenta en GitHub
- Cuenta en Railway (backend)
- Cuenta en Vercel (frontend)
- Variables de entorno configuradas

---

## 🚀 Despliegue del Backend en Railway

### Paso 1: Preparar el Repositorio

```bash
# Asegurar que tenemos Dockerfile
# Confirmar que requirements.txt esté actualizado
git add .
git commit -m "Setup para Railway"
git push origin main
```

### Paso 2: Crear Proyecto en Railway

1. Ir a https://railway.app
2. Click en **New Project**
3. Seleccionar **Deploy from GitHub repo**
4. Conectar tu cuenta de GitHub
5. Seleccionar el repositorio `hackaton2026`

### Paso 3: Configurar Variables de Entorno

1. En Railway, ir a **Variables**
2. Agregar las siguientes variables:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/ai_project_db

# API Keys
OPENAI_API_KEY=sk-your-openai-key
GEMINI_API_KEY=your-gemini-key
KIMI_API_KEY=your-kimi-key

# Security
SECRET_KEY=your-secret-key-here
DEBUG=False

# CORS
ALLOWED_ORIGINS=["https://tu-frontend.vercel.app", "https://otro-dominio.com"]
```

**Obtener DATABASE_URL**:
1. En Railway, agregar servicio **PostgreSQL**
2. Copiar la URL de conexión
3. Pegar en `DATABASE_URL`

### Paso 4: Deploy

1. Railway detectará automáticamente el `Dockerfile`
2. Hará build y deploy automáticamente
3. Esperar a que el status sea **Running**
4. Copiar la URL del proyecto (ej: `https://mi-proyecto-ai-prod.railway.app`)

### Paso 5: Verificar

```bash
# Verificar health check
curl https://mi-proyecto-ai-prod.railway.app/health

# Debería responder:
# {"status": "ok"}
```

---

## 🎨 Despliegue del Frontend en Vercel

### Paso 1: Preparar el Código

```bash
# Ir a carpeta del frontend
cd frontend

# Instalar dependencias localmente
npm install

# Verificar que funciona
npm run build

# Si build es exitoso, hacer push
git add .
git commit -m "Frontend listo para Vercel"
git push origin main
```

### Paso 2: Conectar con Vercel

1. Ir a https://vercel.com
2. Click en **Add New Project**
3. Seleccionar **Import Git Repository**
4. Conectar con GitHub
5. Seleccionar el repositorio

### Paso 3: Configurar Build Settings

Vercel debería detectar automáticamente:
- **Framework**: React
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

Si no, configurar manualmente:

```
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### Paso 4: Agregar Variables de Entorno

1. En Vercel, ir a **Settings > Environment Variables**
2. Agregar:

```
VITE_API_URL=https://mi-proyecto-ai-prod.railway.app
```

### Paso 5: Deploy

1. Click en **Deploy**
2. Esperar a que se complete
3. Se generará una URL automática (ej: `https://mi-proyecto-ai.vercel.app`)

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Opcional)

Crear archivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      
      - name: Run tests
        run: |
          # pytest backend/tests

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: |
          # Implementar deploy script
```

---

## 🗄️ Migración de Base de Datos

### Primera vez (Desde Railway)

```bash
# Conectarse a Railway
ssh your-railway-container

# Crear tablas
python -m alembic upgrade head
```

### Con Alembic (Recomendado)

1. Instalar alembic:
```bash
pip install alembic
alembic init migrations
```

2. Crear migración:
```bash
alembic revision --autogenerate -m "Initial schema"
```

3. Aplicar en producción:
```bash
alembic upgrade head
```

---

## 📊 Monitoreo en Producción

### Railway Dashboard

1. Ver logs en tiempo real
2. Monitorear uso de CPU/Memoria
3. Alertas automáticas
4. Configurar webhooks

### Vercel Analytics

1. Dashboard automático
2. Web Vitals
3. Performance tracking
4. Error reporting

---

## 🐛 Troubleshooting

### Error: "DATABASE_URL not set"
- Verificar que la variable está en Railway
- Restart del deployment

### Error: "API Key invalid"
- Verificar que las keys son correctas
- Regenerar keys si es necesario
- Restart del deployment

### Frontend no puede conectar al backend
- Verificar CORS configurado en Railway
- Verificar `VITE_API_URL` en Vercel
- Comprobar que Railway esté running

### Build falla en Vercel
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📝 Checklist Pre-Deploy

- [ ] Todas las variables de entorno configuradas
- [ ] Database migrada y activa
- [ ] Tests pasando localmente
- [ ] Build de frontend exitoso
- [ ] Dockerfile testado localmente
- [ ] CORS configurado correctamente
- [ ] API Keys validadas
- [ ] Documentación actualizada
- [ ] Git repository sincronizado

---

## 🔐 Seguridad en Producción

### Recomendaciones

1. **Secrets Management**
   - Usar Railway Secrets para API keys
   - Nunca commitear `.env`
   - Rotar keys regularmente

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   @app.post("/api/v1/process-ai")
   @limiter.limit("100/minute")
   async def process_ai(...):
       pass
   ```

3. **HTTPS**
   - Railway incluye SSL automaticamente
   - Vercel incluye SSL automaticamente

4. **CORS Restringido**
   ```python
   ALLOWED_ORIGINS = [
       "https://mi-proyecto.vercel.app",
       "https://www.mi-proyecto.com"
   ]
   ```

---

## 📞 Soporte y Recursos

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

## 🎯 Próximos Pasos

1. Configurar monitoring
2. Implementar logging centralizado
3. Agregar tests automáticos
4. Configurar backups de BD
5. Implementar CDN para archivos estáticos
