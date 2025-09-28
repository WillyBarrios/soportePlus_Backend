# SoportePlus Backend

Un backend API REST desarrollado con Flask para el sistema SoportePlus.

## 🚀 Características

- **Framework**: Flask con arquitectura modular
- **Base de datos**: PostgreSQL (desarrollo) / SQLite (local)
- **Autenticación**: JWT tokens
- **Validación**: Marshmallow schemas
- **Migraciones**: Flask-Migrate
- **CORS**: Configurado para desarrollo frontend
- **Documentación**: API endpoints documentados

## 📁 Estructura del Proyecto

```
soportePlus_Backend/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Blueprints y rutas
│   ├── services/        # Lógica de negocio
│   ├── utils/           # Utilidades y helpers
│   └── __init__.py      # Factory de aplicación
├── config/
│   ├── config.py        # Configuraciones por entorno
│   └── __init__.py
├── migrations/          # Migraciones de base de datos
├── tests/              # Tests unitarios
├── instance/           # Archivos de instancia
├── .env                # Variables de entorno (local)
├── .env.example        # Ejemplo de variables de entorno
├── requirements.txt    # Dependencias de producción
├── requirements-dev.txt # Dependencias de desarrollo
└── run.py             # Punto de entrada de la aplicación
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.9+
- PostgreSQL (para producción)

### Configuración del Entorno

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd soportePlus_Backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   # Dependencias de producción
   pip install -r requirements.txt
   
   # Para desarrollo (incluye herramientas adicionales)
   pip install -r requirements-dev.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Inicializar base de datos**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   
   # Crear usuario administrador
   flask create-admin
   ```

## 🏃‍♂️ Ejecución

### Desarrollo
```bash
python run.py
```

### Producción con Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

La aplicación estará disponible en `http://localhost:5000`

## 📋 API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual (requiere auth)

### Usuarios
- `GET /api/users/` - Listar usuarios (admin)
- `GET /api/users/<id>` - Obtener usuario específico

### General
- `GET /` - Información de la API
- `GET /health` - Health check

### Ejemplo de Registro
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario1",
    "email": "usuario@ejemplo.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

### Ejemplo de Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario1",
    "password": "password123"
  }'
```

## 🗄️ Base de Datos

### Migraciones
```bash
# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir migración
flask db downgrade
```

### Modelos Incluidos
- **User**: Usuario del sistema con autenticación
- **BaseModel**: Modelo base con campos comunes (id, created_at, updated_at)

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app

# Tests específicos
pytest tests/test_auth.py
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `FLASK_ENV` | Entorno de Flask | `development` |
| `SECRET_KEY` | Clave secreta de Flask | `your-secret-key` |
| `JWT_SECRET_KEY` | Clave secreta para JWT | `your-jwt-secret` |
| `DATABASE_URL` | URL de base de datos | `postgresql://user:pass@localhost/db` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS | `http://localhost:3000` |

### Configuraciones por Entorno

- **Development**: Debug habilitado, SQLite local
- **Production**: Debug deshabilitado, PostgreSQL, configuraciones de seguridad
- **Testing**: Base de datos en memoria, configuraciones de prueba

## 📦 Dependencias Principales

- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM
- **Flask-Migrate**: Migraciones de BD
- **Flask-JWT-Extended**: Autenticación JWT
- **Flask-CORS**: Manejo de CORS
- **Marshmallow**: Validación y serialización
- **PostgreSQL**: Base de datos principal
- **Gunicorn**: Servidor WSGI para producción

## 🔐 Seguridad

- Autenticación basada en JWT tokens
- Passwords hasheados con Werkzeug
- CORS configurado apropiadamente
- Headers de seguridad en producción
- Validación de entrada con Marshmallow

## 📝 Comandos CLI Útiles

```bash
# Inicializar base de datos
flask init-db

# Crear usuario administrador
flask create-admin

# Shell interactivo con contexto de app
flask shell
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

---

¿Necesitas ayuda? Abre un issue en el repositorio.