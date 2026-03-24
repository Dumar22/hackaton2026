# Guía de API - Mi Proyecto AI

## Base URL

```
Desarrollo: http://localhost:8000
Producción: https://mi-proyecto-ai-prod.railway.app
```

## Autenticación

Se utiliza JWT (JSON Web Tokens) con el header `Authorization`.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/api/v1/...
```

---

## 📚 Endpoints

### 1. Health Check

Verifica que la API esté activa.

```http
GET /health
```

**Response (200 OK)**:
```json
{
  "status": "ok"
}
```

---

### 2. Procesar Contenido con IA

Procesa un archivo con el modelo de IA especificado.

```http
POST /api/v1/process-ai
Content-Type: multipart/form-data

Parameters:
- file (required): Binary - Archivo a procesar
- model (optional): string - Modelo (gpt, gemini, kimi)
```

**Request Example**:
```bash
curl -X POST http://localhost:8000/api/v1/process-ai \
  -F "file=@document.txt" \
  -F "model=gpt"
```

**Response (200 OK)**:
```json
{
  "success": true,
  "result": {
    "model": "gpt-4",
    "response": "Esta es la respuesta del modelo GPT...",
    "usage": {
      "prompt_tokens": 45,
      "completion_tokens": 120,
      "total_tokens": 165
    }
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "detail": "Tipo de archivo no soportado: application/json"
}
```

**Tipos de Archivo Soportados**:
- `text/plain` (.txt)
- `application/pdf` (.pdf)
- `text/csv` (.csv)
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (.docx)

**Tamaño Máximo**: 50MB

---

### 3. Obtener Modelos Disponibles

Lista todos los modelos de IA disponibles.

```http
GET /api/v1/models
```

**Response (200 OK)**:
```json
{
  "models": [
    "gpt",
    "gemini",
    "kimi"
  ],
  "description": "Modelos de IA disponibles"
}
```

---

## 🔄 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| `200` | OK - Solicitud exitosa |
| `201` | Created - Recurso creado |
| `400` | Bad Request - Solicitud inválida |
| `401` | Unauthorized - Falta autenticación |
| `403` | Forbidden - No autorizado |
| `404` | Not Found - Recurso no encontrado |
| `500` | Internal Server Error - Error del servidor |

---

## 📖 Ejemplos en Diferentes Lenguajes

### JavaScript/Node.js

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function processFile() {
  const form = new FormData();
  form.append('file', fs.createReadStream('document.txt'));
  form.append('model', 'gpt');

  try {
    const response = await axios.post(
      'http://localhost:8000/api/v1/process-ai',
      form,
      { headers: form.getHeaders() }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error.response.data);
  }
}

processFile();
```

### Python

```python
import requests

def process_file():
    url = 'http://localhost:8000/api/v1/process-ai'
    
    with open('document.txt', 'rb') as f:
        files = {'file': f}
        data = {'model': 'gpt'}
        
        response = requests.post(url, files=files, data=data)
        print(response.json())

process_file()
```

### cURL

```bash
# Procesar archivo
curl -X POST http://localhost:8000/api/v1/process-ai \
  -F "file=@document.txt" \
  -F "model=gemini"

# Obtener modelos
curl http://localhost:8000/api/v1/models

# Health check
curl http://localhost:8000/health
```

---

## 🧪 Testing con Postman

1. **Crear nueva request**
   - Tipo: POST
   - URL: `http://localhost:8000/api/v1/process-ai`

2. **Headers**:
   ```
   Authorization: Bearer YOUR_TOKEN
   ```

3. **Body** (form-data):
   ```
   Key: file     | Value: [Seleccionar archivo]
   Key: model    | Value: gpt
   ```

4. **Send**

---

## ⚠️ Manejo de Errores

### Ejemplo: Archivo No Soportado

```json
{
  "detail": "Tipo de archivo no soportado: application/json"
}
```

### Ejemplo: Archivo Muy Grande

```json
{
  "detail": "Archivo demasiado grande: 52428800 bytes"
}
```

### Ejemplo: Error de API Externa

```json
{
  "success": false,
  "error": "No se pudo conectar a la API de GPT",
  "model": "gpt-4"
}
```

---

## 🔗 Rate Limiting

Actualmente no hay límite de rate, pero se recomienda implementar:

- **Producción**: 100 requests/minuto por usuario
- **Desarrollo**: Sin límite

Se implementará en futuras versiones.

---

## 📋 Versioning

La API usa versionado URL:
- `v1` - Versión actual
- `v2` - Próxima versión (planificada)

---

## 📞 Soporte

Si encuentras problemas:
1. Verifica los logs del servidor
2. Valida el formato del request
3. Asegúrate de que las API keys sean válidas
4. Contacta al equipo de desarrollo
