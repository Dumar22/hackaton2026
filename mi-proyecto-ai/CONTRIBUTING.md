# Contribucion Guide - Mi Proyecto AI

## 🎯 Antes de Contribuir

1. Fork el repositorio
2. Clonar tu fork
3. Crear una rama para tu feature

```bash
git clone https://github.com/TU_USUARIO/hackaton2026.git
cd hackaton2026/mi-proyecto-ai
git checkout -b feature/mi-feature
```

---

## 📋 Commit Messages

Usamos el estándar de Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Tipos
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (sin lógica)
- `refactor`: Refactorización de código
- `test`: Agregar o actualizar tests
- `chore`: Mantenimiento

### Ejemplos
```
feat(api): agregar endpoint de procesamiento
fix(frontend): corregir validación de archivos
docs(deployment): actualizar guía de Railway
```

---

## ✅ Checklist Antes de Hacer PR

- [ ] Código formateado (`black`, `eslint`)
- [ ] Tests pasando (`pytest`, `npm test`)
- [ ] Documentación actualizada
- [ ] Sin conflictos con `main`
- [ ] Commits limpios y descriptivos
- [ ] Branch actualizado con `main`

---

## 🧪 Ejecutar Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

---

## 🎨 Estilo de Código

### Backend (Python)

```bash
# Formatear con Black
black app/

# Linting con Flake8
flake8 app/ --max-line-length=100

# Type checking
mypy app/
```

### Frontend (JavaScript)

```bash
# Linting
npm run lint

# Formatear
npm run format
```

---

## 📝 Descripción del PR

Tu PR debe incluir:

```markdown
## Descripción
Breve descripción de los cambios

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Cambio de documentación

## Cómo testearlo
Pasos para verificar los cambios

## Screenshots (si aplica)
Adjuntar screenshots

## Checklist
- [ ] Código testeado
- [ ] Documentación actualizada
- [ ] Sin breaking changes
```

---

## 📚 Estructura de Carpetas

**Agregar nuevos endpoints**: `app/api/v1/`
**Agregar lógica**: `app/services/`
**Agregar integraciones**: `app/integrations/`
**Agregar componentes**: `frontend/src/components/`

---

## 🚀 Antes de Mergear

1. Revisor aprueba cambios
2. Todos los tests pasan
3. Código está formateado
4. Documentación está actualizada

---

## 📞 Preguntas?

Abre un issue o contacta al equipo de desarrollo.

¡Gracias por contribuir! 🎉
