# SoportePlus Backend

Sistema de gestión de tickets de soporte técnico desarrollado con Flask y conectado a base de datos MySQL remota.

## 🚀 Características

- **Autenticación JWT**: Sistema completo de login/logout con tokens seguros basado en email
- **Gestión de Usuarios**: Sistema de roles (Administrador/Técnico)
- **Gestión de Tickets**: CRUD completo para tickets de soporte
- **Base de Datos Remota**: Conectado a servidor MySQL/MariaDB en Linux (173.214.172.154)
- **API RESTful**: Endpoints bien documentados y estructurados
- **Arquitectura Modular**: Blueprints organizados por funcionalidad

## 🛠️ Tecnologías

- **Backend**: Flask 2.3.3
- **Base de Datos**: MySQL/MariaDB remoto con PyMySQL
- **ORM**: SQLAlchemy 2.0.21
- **Autenticación**: Flask-JWT-Extended 4.5.3
- **Validación**: Marshmallow 3.20.1
- **CORS**: Flask-CORS configurado
- **Migraciones**: Flask-Migrate 4.0.5

## 📊 Estructura de la Base de Datos

### Base de Datos Remota
- **Servidor**: Linux 173.214.172.154
- **Base de datos**: `soporteplus`
- **Usuario**: `wbarrios`
- **Conexión**: `mysql+pymysql://wbarrios:Coconut%202112.@173.214.172.154/soporteplus`

### Tablas del Sistema (12 tablas):
- `Usuario` - Usuarios del sistema con roles
- `Tiquet` - Tickets de soporte técnico
- `Cat_tiquet` - Categorías de tickets
- `Estado_tiquet` - Estados de tickets (Abierto, En proceso, Cerrado, etc.)
- `Catalogo_criticidad` - Niveles de criticidad (Baja, Media, Alta, Crítica)
- `Ubicaciones` - Ubicaciones físicas/departamentos
- `Comentarios` - Comentarios de tickets
- `Log_transaccional` - Auditoría de transacciones
- `Cat_problema` - Categorías de problemas
- `Prioridades` - Niveles de prioridad
- `Empleados` - Información de empleados
- `Clientes` - Información de clientes

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/WillyBarrios/soportePlus_Backend.git
cd soportePlus_Backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` con:
```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# Remote Database Configuration


# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 5. Ejecutar la aplicación
```bash
python run.py
# O alternativamente:
flask run
```

La aplicación estará disponible en `http://localhost:5000`

## 📚 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión con email/password
- `GET /api/auth/me` - Obtener información del usuario actual

### Tickets
- `GET /api/tickets/tickets` - Listar todos los tickets
- `POST /api/tickets/tickets` - Crear nuevo ticket
- `PUT /api/tickets/tickets/<id>` - Actualizar ticket existente
- `DELETE /api/tickets/tickets/<id>` - Eliminar ticket

### Catálogos de Soporte
- `GET /api/tickets/categorias` - Obtener categorías de tickets
- `GET /api/tickets/estados` - Obtener estados disponibles
- `GET /api/tickets/criticidades` - Obtener niveles de criticidad
- `GET /api/tickets/ubicaciones` - Obtener ubicaciones disponibles
- `GET /api/tickets/dashboard/stats` - Obtener estadísticas del dashboard

## 🔐 Autenticación

### Login con Email
```bash
POST /api/auth/login
Content-Type: application/json

{
    "email": "jadmin@gmail.com",
    "password": "secret123"
}
```

**Respuesta exitosa:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "jadmin@gmail.com",
        "nombre": "Jesus",
        "apellido": "Admin",
        "tipo_usuario": "Administrador"
    }
}
```

### Usar Token en Requests
```bash
Authorization: Bearer <access_token>
```

## 👥 Usuarios del Sistema

### Usuarios Administradores:
- **Email**: `jadmin@gmail.com` / **Password**: `secret123`
- **Email**: `madmin@gmail.com` / **Password**: `secret123`

### Usuarios Técnicos:
- **Email**: `padmin@test.com` / **Password**: `secret123`
- **Email**: `aadmin@test.com` / **Password**: `secret123`

Todos los usuarios tienen passwords hasheados con SHA-256 en la base de datos.

## 📁 Estructura del Proyecto

```
soportePlus_Backend/
├── app/
│   ├── __init__.py          # Factory de aplicación Flask
│   ├── models/
│   │   ├── __init__.py      # Exports de modelos
│   │   └── soporteplus_models.py  # Modelos SQLAlchemy (12 tablas)
│   ├── routes/
│   │   ├── __init__.py      # Registro de blueprints
│   │   ├── auth.py          # Autenticación JWT con email
│   │   ├── main.py          # Rutas principales
│   │   ├── tickets.py       # CRUD de tickets y catálogos
│   │   └── users.py         # Gestión de usuarios
│   ├── services/            # Lógica de negocio
│   │   └── __init__.py
│   └── utils/
│       ├── __init__.py
│       └── error_handlers.py  # Manejadores de errores
├── config/
│   ├── __init__.py
│   └── config.py            # Configuraciones por entorno
├── migrations/              # Migraciones Flask-Migrate
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── ea2496fd28b6_initial_migration.py
├── tests/                   # Tests unitarios
│   ├── __init__.py
│   └── test_basic.py
├── .gitignore              # Archivos excluidos de Git
├── requirements.txt        # Dependencias de producción
├── requirements-dev.txt    # Dependencias de desarrollo
├── pyproject.toml         # Configuración del proyecto
└── run.py                 # Punto de entrada de la aplicación
```

## 🔧 Desarrollo

### Ejecutar en modo desarrollo
```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar con debug habilitado
python run.py
```

### Gestión de Base de Datos
```bash
# Aplicar migraciones (si es necesario)
flask db upgrade

# Crear nueva migración
flask db migrate -m "Descripción del cambio"
```

### Testing
```bash
# Ejecutar tests básicos
python -m pytest tests/
```

## 🌐 Configuración de Producción

### Servidor Remoto
La aplicación está configurada para conectarse a:
- **Host**: Servidor Linux remoto (173.214.172.154)
- **Base de datos**: `soporteplus`
- **Puerto**: 3306 (MySQL estándar)
- **SSL**: Conexión segura configurada



## 📦 Dependencias Principales

- **Flask 2.3.3** - Framework web principal
- **SQLAlchemy 2.0.21** - ORM para base de datos
- **PyMySQL 1.1.0** - Driver MySQL/MariaDB
- **Flask-JWT-Extended 4.5.3** - Autenticación JWT
- **Flask-CORS** - Manejo de CORS para frontend
- **Marshmallow 3.20.1** - Validación y serialización
- **Flask-Migrate 4.0.5** - Migraciones de base de datos

## 🚀 Despliegue

### Usando Gunicorn (Recomendado para producción)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Usando Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

## 🛡️ Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Passwords Hash**: SHA-256 en base de datos
- **CORS Configurado**: Solo orígenes permitidos
- **Validación de Entrada**: Marshmallow schemas
- **Base de Datos Remota**: Conexión segura a servidor Linux

## 📝 Ejemplos de Uso

### Crear un Ticket
```bash
curl -X POST http://localhost:5000/api/tickets/tickets \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Problema con impresora",
    "descripcion": "La impresora no responde",
    "id_categoria": 1,
    "id_criticidad": 2,
    "id_ubicacion": 1
  }'
```

### Obtener Categorías
```bash
curl -X GET http://localhost:5000/api/tickets/categorias \
  -H "Authorization: Bearer <token>"
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es de uso interno para el sistema de soporte técnico.

## 👨‍💻 Desarrolladores

**Equipo de Desarrollo SoportePlus**
- **Lead Developer**: Willy Barrios
- **GitHub**: [@WillyBarrios](https://github.com/WillyBarrios)
- **Año**: 2025

---

### 📋 Estado del Proyecto

✅ **Backend completo y funcional**  
✅ **Base de datos remota configurada**  
✅ **Autenticación JWT implementada**  
✅ **4 usuarios reales migrados**  
✅ **12 tablas de base de datos operativas**  
✅ **API REST completamente documentada**  
✅ **Listo para integración con frontend**

---

*Para soporte técnico o preguntas sobre la implementación, contactar al equipo de desarrollo.*