# Guía de Instalación - Asistente de Presupuestos HDL

Esta guía te ayudará a instalar y configurar el sistema completo del Asistente Inteligente de Presupuestos.

## 📋 Requisitos Previos

### Sistema Operativo
- **Linux:** Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **macOS:** 10.15+ (Catalina o superior)
- **Windows:** 10/11 con WSL2 (recomendado)

### Software Requerido

#### Node.js y npm
```bash
# Verificar instalación
node --version  # v18.0.0 o superior
npm --version   # v8.0.0 o superior

# Instalar en Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar en macOS
brew install node

# Instalar en Windows
# Descargar desde https://nodejs.org/
```

#### Python 3.11+
```bash
# Verificar instalación
python3 --version  # 3.11.0 o superior

# Instalar en Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Instalar en macOS
brew install python@3.11

# Instalar en Windows
# Descargar desde https://python.org/downloads/
```

#### Git
```bash
# Verificar instalación
git --version

# Instalar en Ubuntu/Debian
sudo apt install git

# Instalar en macOS
brew install git

# Instalar en Windows
# Descargar desde https://git-scm.com/
```

## 🚀 Instalación Automática (Recomendada)

### Opción 1: Script de Instalación
```bash
# Clonar o descargar el proyecto
cd asistente-presupuestos-hdl

# Dar permisos de ejecución
chmod +x scripts/setup.sh

# Ejecutar instalación automática
./scripts/setup.sh
```

El script automáticamente:
- ✅ Verifica requisitos del sistema
- ✅ Instala dependencias del backend
- ✅ Instala dependencias del frontend
- ✅ Configura variables de entorno
- ✅ Ejecuta tests básicos
- ✅ Inicia ambos servidores

## 🔧 Instalación Manual

### Paso 1: Preparar el Entorno

```bash
# Navegar al directorio del proyecto
cd asistente-presupuestos-hdl

# Crear directorios de logs y datos
mkdir -p logs data/budgets data/knowledge
```

### Paso 2: Configurar Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear entorno virtual
python3.11 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python src/main.py --version
```

### Paso 3: Configurar Frontend

```bash
# Navegar al directorio del frontend (nueva terminal)
cd frontend

# Instalar dependencias
npm install

# Verificar instalación
npm run build
```

### Paso 4: Configurar Variables de Entorno

```bash
# Crear archivo de configuración del backend
cd backend
cp .env.example .env

# Editar configuración
nano .env
```

Contenido del archivo `.env`:
```bash
# Configuración del servidor
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# APIs HDL Zomatik
HDL_API_BASE=https://hdl.zomatik.com/ws_web.php
HDL_API_TIMEOUT=30

# IA (Opcional - para funcionalidades avanzadas)
OPENAI_API_KEY=tu_clave_openai_aqui
OPENAI_API_BASE=https://api.openai.com/v1

# Base de datos (Opcional)
DATABASE_URL=sqlite:///data/app.db

# Configuración de archivos
UPLOAD_FOLDER=data/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Paso 5: Inicializar Base de Datos

```bash
# Desde el directorio backend
cd backend
source venv/bin/activate

# Crear tablas de base de datos
python -c "
from src.main import app
from src.models.user import db
with app.app_context():
    db.create_all()
    print('Base de datos inicializada')
"
```

## 🧪 Verificación de la Instalación

### Test del Backend
```bash
cd backend
source venv/bin/activate

# Iniciar servidor de desarrollo
python src/main.py

# En otra terminal, verificar endpoints
curl http://localhost:5000/
curl http://localhost:5000/api/chat/societies
```

### Test del Frontend
```bash
cd frontend

# Iniciar servidor de desarrollo
npm run dev

# Verificar en navegador
# http://localhost:5173
```

### Test de Integración
```bash
# Ejecutar tests automáticos
cd backend
python -m pytest tests/

cd ../frontend
npm run test
```

## 🐳 Instalación con Docker (Alternativa)

### Requisitos
- Docker 20.10+
- Docker Compose 2.0+

### Instalación
```bash
# Construir y ejecutar contenedores
docker-compose up -d

# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Configuración Docker
El archivo `docker-compose.yml` incluye:
- ✅ Contenedor del backend (Flask)
- ✅ Contenedor del frontend (Nginx)
- ✅ Base de datos PostgreSQL
- ✅ Redis para cache
- ✅ Volúmenes persistentes

## 🔧 Configuración Avanzada

### Proxy Reverso (Nginx)
```nginx
# /etc/nginx/sites-available/asistente-hdl
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL/HTTPS (Certbot)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Base de Datos PostgreSQL
```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb asistente_hdl

# Crear usuario
sudo -u postgres createuser --interactive asistente_user

# Configurar en .env
DATABASE_URL=postgresql://asistente_user:password@localhost/asistente_hdl
```

## 🚀 Puesta en Producción

### Usando Gunicorn (Backend)
```bash
cd backend
source venv/bin/activate

# Instalar Gunicorn
pip install gunicorn

# Ejecutar en producción
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

### Build de Producción (Frontend)
```bash
cd frontend

# Crear build optimizado
npm run build

# Servir con servidor web
sudo cp -r dist/* /var/www/html/
```

### Systemd Services
```bash
# Crear servicio del backend
sudo nano /etc/systemd/system/asistente-hdl-backend.service
```

Contenido del servicio:
```ini
[Unit]
Description=Asistente HDL Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/asistente-presupuestos-hdl/backend
Environment=PATH=/path/to/asistente-presupuestos-hdl/backend/venv/bin
ExecStart=/path/to/asistente-presupuestos-hdl/backend/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y iniciar servicio
sudo systemctl enable asistente-hdl-backend
sudo systemctl start asistente-hdl-backend
sudo systemctl status asistente-hdl-backend
```

## 🔍 Troubleshooting

### Problemas Comunes

#### Error: "Module not found"
```bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### Error: "Port already in use"
```bash
# Encontrar proceso usando el puerto
sudo lsof -i :5000
sudo lsof -i :5173

# Terminar proceso
sudo kill -9 <PID>
```

#### Error: "Permission denied"
```bash
# Dar permisos correctos
chmod +x scripts/*.sh
sudo chown -R $USER:$USER .
```

#### Error de CORS
```bash
# Verificar configuración en backend/src/main.py
# Asegurar que CORS esté habilitado para el dominio correcto
```

### Logs y Debugging

#### Backend Logs
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Logs de Gunicorn
tail -f /var/log/gunicorn/error.log
```

#### Frontend Logs
```bash
# Logs de desarrollo
npm run dev

# Logs de build
npm run build --verbose
```

### Monitoreo

#### Health Checks
```bash
# Script de monitoreo
#!/bin/bash
# health-check.sh

# Verificar backend
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Backend OK"
else
    echo "❌ Backend DOWN"
fi

# Verificar frontend
if curl -f http://localhost:5173/ > /dev/null 2>&1; then
    echo "✅ Frontend OK"
else
    echo "❌ Frontend DOWN"
fi
```

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. **Revisa los logs** en `logs/app.log`
2. **Verifica requisitos** del sistema
3. **Consulta la documentación** en `docs/`
4. **Contacta soporte técnico:**
   - Email: soporte@hdl.com.ar
   - Teléfono: (011) 4567-8900

## 🔄 Actualizaciones

Para actualizar el sistema:

```bash
# Hacer backup
./scripts/backup.sh

# Actualizar código
git pull origin main

# Actualizar dependencias
cd backend && pip install -r requirements.txt --upgrade
cd ../frontend && npm update

# Reiniciar servicios
./scripts/restart.sh
```

