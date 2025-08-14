# Asistente de Presupuestos - Backend

API Flask para el asistente inteligente de presupuestos de corralón HDL.

## Características

- 🚀 API RESTful con Flask
- 🤖 Servicio de IA conversacional
- 📄 Generación de PDFs profesionales
- 🔗 Integración con APIs HDL Zomatik
- 💾 Gestión de base de conocimiento
- 🌐 CORS habilitado para frontend

## Tecnologías

- **Flask** - Framework web
- **ReportLab** - Generación de PDFs
- **Requests** - Cliente HTTP para APIs externas
- **Flask-CORS** - Manejo de CORS
- **Python 3.11** - Lenguaje base

## Instalación

1. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar servidor:**
   ```bash
   python src/main.py
   ```

4. **Verificar funcionamiento:**
   ```bash
   curl http://localhost:5000/
   ```

## Estructura del Proyecto

```
src/
├── routes/
│   ├── chat.py               # Endpoints de conversación
│   ├── budget.py             # Endpoints de presupuestos
│   └── knowledge.py          # Endpoints de conocimiento
├── services/
│   ├── simple_ai_service.py  # Servicio de IA simplificado
│   ├── hdl_api.py           # Integración APIs HDL
│   ├── pdf_service.py       # Generación de PDFs
│   └── mock_data.py         # Datos de prueba
├── models/                   # Modelos de datos (SQLAlchemy)
└── main.py                  # Aplicación Flask principal
```

## APIs Implementadas

### Chat (`/api/chat/`)
- `POST /message` - Procesar mensajes del usuario
- `GET /societies` - Obtener sociedades HDL
- `GET /search-products` - Buscar productos

### Presupuestos (`/api/budget/`)
- `POST /generate` - Generar presupuesto
- `POST /generate-pdf` - Crear PDF
- `POST /save` - Guardar presupuesto
- `GET /list` - Listar presupuestos
- `GET /<id>` - Obtener presupuesto específico

### Conocimiento (`/api/knowledge/`)
- `GET /list` - Listar conocimiento
- `POST /add` - Agregar conocimiento
- `GET /<id>` - Obtener conocimiento específico
- `PUT /<id>` - Actualizar conocimiento
- `DELETE /<id>` - Eliminar conocimiento
- `POST /search` - Buscar en conocimiento

## Servicios

### SimpleAIService
Servicio de IA simplificado que maneja:
- Clasificación de mensajes
- Generación de respuestas contextuales
- Detección de necesidad de búsqueda
- Resúmenes de presupuestos

### HDLApiService
Integración con APIs HDL Zomatik:
- Operación 1: Obras y listas de precios
- Operación 2: Sucursales y sociedades
- Operación 3: Catálogo de artículos

### PDFService
Generación de PDFs profesionales:
- Formato empresarial con logo
- Tablas detalladas de productos
- Cálculos automáticos de totales
- Información de contacto

## Configuración

### Variables de Entorno
```bash
# Opcional: Para IA avanzada
OPENAI_API_KEY=tu_clave_openai
OPENAI_API_BASE=https://api.openai.com/v1

# URLs de APIs HDL (ya configuradas)
HDL_API_BASE=https://hdl.zomatik.com/ws_web.php
```

### Modo de Desarrollo
El servicio HDL tiene un modo de prueba que usa datos mock cuando las APIs no están disponibles.

## Almacenamiento

### Presupuestos
Se guardan en `/tmp/budgets/` como archivos JSON.

### Conocimiento
Se almacena en `/tmp/knowledge/` como archivos JSON.

### PDFs Temporales
Se generan en `/tmp/` y se envían al cliente.

## Ejemplos de Uso

### Enviar Mensaje al Chat
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Necesito cemento para una obra",
    "conversation_history": []
  }'
```

### Generar Presupuesto
```bash
curl -X POST http://localhost:5000/api/budget/generate \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "codigo": "CEM001",
        "nombre": "Cemento Portland",
        "cantidad": 10,
        "precio_unitario": 1500,
        "total": 15000
      }
    ],
    "client_info": {
      "name": "Juan Pérez",
      "email": "juan@email.com"
    }
  }'
```

### Agregar Conocimiento
```bash
curl -X POST http://localhost:5000/api/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Información de la empresa",
    "content": "HDL es un corralón especializado...",
    "category": "empresa"
  }'
```

## Desarrollo

### Agregar Nuevos Endpoints
1. Crear archivo en `src/routes/`
2. Definir Blueprint
3. Registrar en `main.py`

### Agregar Nuevos Servicios
1. Crear archivo en `src/services/`
2. Implementar clase de servicio
3. Importar en rutas necesarias

### Testing
```bash
# Verificar APIs HDL
curl "https://hdl.zomatik.com/ws_web.php?operacion=1"

# Verificar servidor local
curl http://localhost:5000/api/budget/list
```

## Deployment

### Producción
Para deployment, usar las herramientas de Manus:
```bash
# Desde el directorio del proyecto
service_deploy_backend flask presupuesto-assistant-backend
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 5000
CMD ["python", "src/main.py"]
```

## Troubleshooting

### Error de Importación
Verificar que el PYTHONPATH incluya el directorio del proyecto:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/presupuesto-assistant-backend"
```

### Error de CORS
Verificar que Flask-CORS esté instalado y configurado en `main.py`.

### APIs HDL No Disponibles
El sistema automáticamente usa datos mock si las APIs no responden.

### Error de ReportLab
Instalar dependencias del sistema:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# CentOS/RHEL
sudo yum install python3-devel
```

## Logs

Los logs se muestran en la consola durante el desarrollo. Para producción, configurar logging apropiado.

## Seguridad

- CORS configurado para desarrollo
- Para producción, restringir orígenes CORS
- Validar todas las entradas de usuario
- Implementar autenticación si es necesario

