# Asistente Inteligente - HDL

Sistema completo de asistente conversacional para generar presupuestos de materiales de construcción, con integración a APIs HDL Zomatik y panel de administración.

## 🚀 Características Principales (fase 1)

- **🤖 Asistente Conversacional:** Chat inteligente que guía al usuario en la creación de presupuestos
- **📊 Integración APIs HDL:** Conexión directa con el sistema HDL Zomatik para datos en tiempo real
- **💼 Generación de PDFs:** Presupuestos profesionales en formato PDF
- **🛠️ Panel de Administración:** Gestión de presupuestos y base de conocimiento
- **📱 Diseño Responsive:** Funciona perfectamente en desktop y móvil

## 📁 Estructura del Proyecto

```
asistente-presupuestos-hdl/
├── README.md                 # Este archivo
├── INSTALL.md               # Guía de instalación completa
├── ARCHITECTURE.md          # Documentación de arquitectura
├── frontend/                # Aplicación React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── services/        # Servicios y APIs
│   │   └── assets/          # Recursos estáticos
│   ├── package.json
│   └── README.md
├── backend/                 # API Flask
│   ├── src/
│   │   ├── routes/          # Endpoints de la API
│   │   ├── services/        # Lógica de negocio
│   │   └── models/          # Modelos de datos
│   ├── requirements.txt
│   └── README.md
├── docs/                    # Documentación completa
│   ├── api-analysis.md      # Análisis de APIs HDL
│   ├── user-guide.md        # Guía de usuario
│   └── deployment.md        # Guía de deployment
├── config/                  # Archivos de configuración
│   ├── docker-compose.yml   # Para deployment con Docker
│   └── nginx.conf           # Configuración de proxy
└── scripts/                 # Scripts de utilidad
    ├── setup.sh             # Script de instalación automática
    ├── start.sh             # Script para iniciar el proyecto
    └── deploy.sh            # Script de deployment
```

## ⚡ Inicio Rápido

### Opción 1: Script Automático
```bash
cd asistente-presupuestos-hdl
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Opción 2: Instalación Manual

1. **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python src/main.py
   ```

2. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Acceder a la aplicación:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## 🛠️ Tecnologías

### Frontend
- **React 18** - Framework de UI
- **Vite** - Build tool
- **shadcn/ui** - Componentes UI
- **Tailwind CSS** - Estilos
- **Lucide React** - Iconos

### Backend
- **Flask** - Framework web
- **Python 3.11** - Lenguaje
- **ReportLab** - Generación de PDFs
- **Flask-CORS** - Manejo de CORS

## 📖 Documentación

- [Guía de Instalación](INSTALL.md) - Instrucciones detalladas de instalación
- [Arquitectura](ARCHITECTURE.md) - Documentación técnica completa
- [Análisis de APIs](docs/api-analysis.md) - Análisis de las APIs HDL Zomatik
- [Guía de Usuario](docs/user-guide.md) - Manual de uso de la aplicación
- [Deployment](docs/deployment.md) - Guía para poner en producción

## 🔧 Configuración

### Variables de Entorno (Opcional)
```bash
# Para IA avanzada (opcional)
OPENAI_API_KEY=tu_clave_openai
OPENAI_API_BASE=https://api.openai.com/v1

# URLs de APIs HDL (ya configuradas)
HDL_API_BASE=https://hdl.zomatik.com/ws_web.php
```

## 🚀 Deployment

### Desarrollo Local
```bash
./scripts/start.sh
```

### Producción
```bash
./scripts/deploy.sh
```

### Docker
```bash
docker-compose up -d
```

## 📊 APIs Integradas

El sistema se integra con 3 endpoints de HDL Zomatik:

1. **Operación 1:** Obras y listas de precios por cliente
2. **Operación 2:** Información de sucursales y sociedades  
3. **Operación 3:** Catálogo completo de artículos con precios

## 🎯 Funcionalidades

### Para Usuarios
- Chat conversacional para solicitar presupuestos
- Búsqueda automática de productos
- Generación de PDFs profesionales
- Interfaz intuitiva y responsive

### Para Administradores
- Dashboard con estadísticas
- Gestión de base de conocimiento
- Historial de presupuestos
- Búsqueda avanzada

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- email: nicolas.seguro@gmail.com

## 🔄 Versiones

- **v1.0.0** - Versión inicial con todas las funcionalidades base
- Chat conversacional ✅
- Integración APIs HDL ✅
- Generación de PDFs ✅
- Panel de administración ✅

---

**Desarrollado para Corralón HDL** 🏗️

