# Esquema de Base de Datos - Mi Proyecto AI

## 📊 Diagrama ER

```
┌─────────────────┐          ┌──────────────────────┐
│     USERS       │          │ PROCESSING_REQUESTS  │
├─────────────────┤          ├──────────────────────┤
│ id (PK)         │◄─────────│ id (PK)              │
│ email (UNIQUE)  │ 1      * │ user_id (FK)         │
│ username        │          │ file_name            │
│ is_active       │          │ model_used           │
│ created_at      │          │ status               │
└─────────────────┘          │ result               │
                             │ error                │
                             │ created_at           │
                             │ updated_at           │
                             └──────────────────────┘
```

---

## 🗂️ Tablas

### 1. USERS

Almacena información de usuarios del sistema.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Campos**:
| Campo | Tipo | Constraint | Descripción |
|-------|------|-----------|-------------|
| `id` | SERIAL | PRIMARY KEY | Identificador único |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Correo del usuario |
| `username` | VARCHAR(100) | UNIQUE, NOT NULL | Nombre de usuario |
| `is_active` | BOOLEAN | DEFAULT TRUE | Estado de la cuenta |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Fecha de creación |

**Índices**:
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);
```

---

### 2. PROCESSING_REQUESTS

Registra todas las solicitudes de procesamiento de IA.

```sql
CREATE TABLE processing_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    file_name VARCHAR(255),
    model_used VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    result TEXT,
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Campos**:
| Campo | Tipo | Constraint | Descripción |
|-------|------|-----------|-------------|
| `id` | SERIAL | PRIMARY KEY | Identificador único |
| `user_id` | INTEGER | NOT NULL, FK | Usuario que hizo la solicitud |
| `file_name` | VARCHAR(255) | | Nombre del archivo |
| `model_used` | VARCHAR(50) | | Modelo utilizado (gpt, gemini, kimi) |
| `status` | VARCHAR(20) | DEFAULT 'pending' | Estado (pending, processing, completed, failed) |
| `result` | TEXT | | Resultado del procesamiento |
| `error` | TEXT | | Mensaje de error si falló |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Fecha de creación |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Última actualización |

**Índices**:
```sql
CREATE INDEX idx_processing_user_id ON processing_requests(user_id);
CREATE INDEX idx_processing_status ON processing_requests(status);
CREATE INDEX idx_processing_created_at ON processing_requests(created_at);
```

---

## 🔄 Relaciones

### Usuarios → Solicitudes (1:N)

Un usuario puede tener muchas solicitudes de procesamiento.

```sql
ALTER TABLE processing_requests 
ADD CONSTRAINT fk_processing_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

- **Tipo**: One-to-Many
- **Cascada**: Al eliminar usuario, elimina sus solicitudes
- **Cardinalidad**: 1 usuario : N solicitudes

---

## 📈 Tamaño Esperado

### Estimaciones para 1 año de operación:

```
Tabla                        Registros      Tamaño Aproximado
─────────────────────────────────────────────────────────────
users                        50,000         5 MB
processing_requests          1,000,000      500 MB
─────────────────────────────────────────────────────────────
Total                                       ~505 MB
```

---

## 🔒 Seguridad

### Constrains de Integridad

```sql
-- Validar que models_used sea uno de los permitidos
ALTER TABLE processing_requests
ADD CONSTRAINT check_model_used
CHECK (model_used IN ('gpt', 'gemini', 'kimi'));

-- Validar que status sea válido
ALTER TABLE processing_requests
ADD CONSTRAINT check_status
CHECK (status IN ('pending', 'processing', 'completed', 'failed'));
```

### Permisos

```sql
-- Crear usuario de aplicación
CREATE USER app_user WITH PASSWORD 'secure_password';

-- Permisos mínimos
GRANT CONNECT ON DATABASE ai_project_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON processing_requests TO app_user;
```

---

## 🚀 Operaciones Comunes

### Crear Database y Tablas

```sql
-- Desde psql
CREATE DATABASE ai_project_db;

\c ai_project_db

-- Ejecutar scripts de creación
\i schema.sql
```

### Insertar Datos de Prueba

```sql
-- Insertar usuario
INSERT INTO users (email, username) 
VALUES ('test@example.com', 'testuser');

-- Insertar solicitud de procesamiento
INSERT INTO processing_requests (user_id, file_name, model_used, status)
VALUES (1, 'document.txt', 'gpt', 'pending');
```

### Queries Útiles

```sql
-- Solicitudes por estado
SELECT COUNT(*) as total, status 
FROM processing_requests 
GROUP BY status;

-- Usuario con más solicitudes
SELECT u.username, COUNT(pr.id) as total_requests
FROM users u
LEFT JOIN processing_requests pr ON u.id = pr.user_id
GROUP BY u.id
ORDER BY total_requests DESC;

-- Últimas 10 solicitudes
SELECT * FROM processing_requests
ORDER BY created_at DESC
LIMIT 10;

-- Modelos más utilizados
SELECT model_used, COUNT(*) as usage_count
FROM processing_requests
GROUP BY model_used
ORDER BY usage_count DESC;
```

---

## 🔄 Migraciones

### Con Alembic

```bash
# Crear carpeta de migraciones
alembic init migrations

# Generar migración automática
alembic revision --autogenerate -m "Crear tablas iniciales"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history

# Revertir última migración
alembic downgrade -1
```

### Archivo de Migración Ejemplo

```python
# migrations/versions/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
```

---

## 📊 Monitoreo

### Queries para Monitoreo

```sql
-- Tamaño de tablas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Conexiones activas
SELECT count(*) as conexiones_activas FROM pg_stat_activity;

-- Queries lentos
SELECT query, calls, mean_time 
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
ORDER BY mean_time DESC
LIMIT 10;
```

---

## 🛠️ Backup y Restore

### Backup Completo

```bash
# Backup en formato SQL
pg_dump -U postgres -F p ai_project_db > backup.sql

# Backup en formato binario (más eficiente)
pg_dump -U postgres -F c ai_project_db > backup.dump

# Con compresión
pg_dump -U postgres -F c -z ai_project_db > backup.dump.gz
```

### Restore

```bash
# Desde archivo SQL
psql -U postgres ai_project_db < backup.sql

# Desde archivo binario
pg_restore -U postgres -d ai_project_db backup.dump
```

---

## 📅 Mantenimiento

### Vacuum y Analyze

```bash
# Conectarse a la BD
psql -U postgres ai_project_db

# Optimizar tablas
VACUUM ANALYZE;

# Vacío completo (requiere lock)
VACUUM FULL;
```

---

## 🔍 Debugging

### Verificar Esquema

```sql
-- Listar tablas
\dt

-- Ver estructura de tabla
\d users

-- Ver índices
\di

-- Ver relaciones
\d+ processing_requests
```

---

## 📝 Notas Importantes

1. **Backups**: Hacer backups regularmente
2. **Índices**: Crear índices para queries frecuentes
3. **Particionamiento**: Para tablas grandes, considerar particionamiento
4. **Vacuuming**: Ejecutar VACUUM regularmente
5. **Monitoreo**: Monitorear crecimiento de BD

---

## 🎓 Recursos

- PostgreSQL Docs: https://www.postgresql.org/docs
- Alembic: https://alembic.sqlalchemy.org
- SQLAlchemy ORM: https://docs.sqlalchemy.org/orm
