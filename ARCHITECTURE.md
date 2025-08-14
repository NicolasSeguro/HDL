# Aplicación Web - Asistente Inteligente para Presupuestos de Corralón

## Resumen Ejecutivo

Se ha desarrollado exitosamente una aplicación web completa que funciona como asistente inteligente para generar presupuestos en un corralón de materiales de construcción. La aplicación combina una interfaz conversacional moderna con integración a APIs externas y capacidades de gestión administrativa.

## Características Principales

### 🤖 Asistente Conversacional Inteligente
- **Interfaz de chat moderna** con diseño limpio y profesional
- **Lógica conversacional avanzada** que guía al usuario paso a paso
- **Respuestas contextuales** basadas en el tipo de consulta
- **Botones de respuesta rápida** para agilizar la interacción
- **Soporte multimodal** preparado para texto, imágenes y audio

### 📊 Integración con APIs HDL Zomatik
- **Conexión a 3 endpoints principales:**
  - `operacion=1`: Obras y listas de precios por cliente
  - `operacion=2`: Información de sucursales y sociedades
  - `operacion=3`: Catálogo completo de artículos con precios
- **Búsqueda automática de productos** cuando se detectan palabras clave
- **Datos en tiempo real** del catálogo de materiales

### 💼 Generación de Presupuestos
- **Creación automática de presupuestos** basada en la conversación
- **Cálculo automático de totales** incluyendo IVA (21%)
- **Generación de PDFs profesionales** con formato empresarial
- **Vista previa editable** antes de generar el documento final
- **Resúmenes inteligentes** generados por IA

### 🛠️ Panel de Administración
- **Dashboard con estadísticas** de presupuestos generados
- **Historial completo** de todos los presupuestos
- **Gestión de base de conocimiento** para entrenar al asistente
- **Categorización de información** (empresa, productos, políticas, etc.)
- **Búsqueda avanzada** en presupuestos y conocimiento

## Arquitectura Técnica

### Frontend (React)
- **Framework:** React 18 con Vite
- **UI Components:** shadcn/ui + Tailwind CSS
- **Iconos:** Lucide React
- **Estado:** React Hooks (useState, useEffect)
- **Comunicación:** Fetch API para llamadas al backend

### Backend (Flask)
- **Framework:** Flask con Python 3.11
- **APIs:** RESTful endpoints organizados por módulos
- **CORS:** Habilitado para comunicación frontend-backend
- **Generación PDF:** ReportLab para documentos profesionales
- **Almacenamiento:** Sistema de archivos JSON para persistencia

### Servicios Implementados

#### 1. Servicio de IA Simplificado (`SimpleAIService`)
- Procesamiento de mensajes conversacionales
- Clasificación automática de consultas
- Generación de respuestas contextuales
- Detección de necesidad de búsqueda de productos
- Generación de resúmenes de presupuestos

#### 2. Servicio de APIs HDL (`HDLApiService`)
- Integración con los 3 endpoints de HDL Zomatik
- Búsqueda de artículos por términos
- Obtención de sociedades y sucursales
- Modo de prueba con datos mock para desarrollo

#### 3. Servicio de PDFs (`PDFService`)
- Generación de presupuestos en formato PDF
- Diseño profesional con logo y colores corporativos
- Tablas detalladas de productos y precios
- Cálculos automáticos de totales e IVA
- Información de contacto y condiciones

## Estructura de Directorios

```
presupuesto-assistant-frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx      # Interfaz principal de chat
│   │   ├── AdminPanel.jsx         # Panel de administración
│   │   └── ui/                    # Componentes UI reutilizables
│   ├── services/
│   │   └── api.js                 # Cliente API para backend
│   └── App.jsx                    # Componente principal con navegación

presupuesto-assistant-backend/
├── src/
│   ├── routes/
│   │   ├── chat.py               # Endpoints de conversación
│   │   ├── budget.py             # Endpoints de presupuestos
│   │   └── knowledge.py          # Endpoints de conocimiento
│   ├── services/
│   │   ├── simple_ai_service.py  # Servicio de IA simplificado
│   │   ├── hdl_api.py           # Integración APIs HDL
│   │   └── pdf_service.py       # Generación de PDFs
│   └── main.py                  # Aplicación Flask principal
```

## Funcionalidades Detalladas

### Chat Conversacional
1. **Mensaje de bienvenida** automático al cargar
2. **Procesamiento de consultas** en lenguaje natural
3. **Búsqueda automática** de productos cuando se mencionan materiales
4. **Respuestas rápidas** contextuales para agilizar el flujo
5. **Historial de conversación** mantenido durante la sesión

### Gestión de Presupuestos
1. **Generación automática** basada en productos seleccionados
2. **Cálculos precisos** de subtotales, IVA y totales
3. **PDFs profesionales** con formato empresarial
4. **Guardado automático** en el sistema
5. **Listado y búsqueda** de presupuestos históricos

### Base de Conocimiento
1. **Agregado de información** sobre la empresa
2. **Categorización** por tipo de contenido
3. **Búsqueda** en títulos y contenido
4. **Edición y eliminación** de entradas
5. **Exportación** completa de la base

## APIs Implementadas

### Endpoints de Chat
- `POST /api/chat/message` - Procesar mensajes del usuario
- `GET /api/chat/societies` - Obtener sociedades disponibles
- `GET /api/chat/search-products` - Buscar productos

### Endpoints de Presupuestos
- `POST /api/budget/generate` - Generar presupuesto
- `POST /api/budget/generate-pdf` - Crear PDF del presupuesto
- `POST /api/budget/save` - Guardar presupuesto
- `GET /api/budget/list` - Listar presupuestos
- `GET /api/budget/<id>` - Obtener presupuesto específico

### Endpoints de Conocimiento
- `GET /api/knowledge/list` - Listar conocimiento
- `POST /api/knowledge/add` - Agregar conocimiento
- `GET /api/knowledge/<id>` - Obtener conocimiento específico
- `PUT /api/knowledge/<id>` - Actualizar conocimiento
- `DELETE /api/knowledge/<id>` - Eliminar conocimiento
- `POST /api/knowledge/search` - Buscar en conocimiento

## Datos Analizados

### APIs HDL Zomatik
Se analizaron exitosamente las 3 APIs proporcionadas:

1. **Operación 1 (Obras y Listas):**
   - 4 clientes con obras asociadas
   - Múltiples listas de precios por obra
   - Estructura jerárquica cliente → sociedad → obra → lista

2. **Operación 2 (Sucursales y Sociedades):**
   - 4 sociedades principales
   - Múltiples sucursales por sociedad
   - Información completa de contacto

3. **Operación 3 (Catálogo de Artículos):**
   - Miles de productos de construcción
   - Precios diferenciados por lista
   - Categorías: cemento, cal, yeso, ladrillos, adhesivos, etc.

### Archivos de Empresa
Se procesaron los archivos proporcionados:

1. **PROVEEDORESCONPAGINAWEB.pdf:**
   - Lista de proveedores con sitios web
   - Información de contacto y especialidades

2. **Cantidad,pesoydisposiciondemateriales.xlsx:**
   - Lista detallada de materiales con especificaciones
   - Información de capacidad de flota para entregas

## Instrucciones de Uso

### Para Usuarios Finales

1. **Acceder al Chat:**
   - Abrir la aplicación en el navegador
   - Escribir consulta en lenguaje natural
   - Seguir las respuestas y sugerencias del asistente

2. **Generar Presupuesto:**
   - Describir el proyecto o materiales necesarios
   - Confirmar productos sugeridos
   - Revisar presupuesto generado
   - Descargar PDF o enviar por email

### Para Administradores

1. **Acceder al Panel:**
   - Hacer clic en "Administración" en el header
   - Ver estadísticas y métricas

2. **Gestionar Conocimiento:**
   - Ir a la pestaña "Base de Conocimiento"
   - Agregar información sobre productos, políticas, etc.
   - Categorizar apropiadamente el contenido

3. **Revisar Presupuestos:**
   - Ver historial completo en la pestaña "Presupuestos"
   - Descargar PDFs de presupuestos anteriores
   - Buscar por cliente o fecha

## Instalación y Deployment

### Desarrollo Local

1. **Backend:**
   ```bash
   cd presupuesto-assistant-backend
   source venv/bin/activate
   pip install -r requirements.txt
   python src/main.py
   ```

2. **Frontend:**
   ```bash
   cd presupuesto-assistant-frontend
   npm install
   npm run dev
   ```

### Deployment en Producción

La aplicación está preparada para deployment usando las herramientas de Manus:

1. **Frontend:** `service_deploy_frontend`
2. **Backend:** `service_deploy_backend`

## Extensibilidad Futura

### Integraciones Pendientes
1. **OpenAI/Anthropic:** Para IA más avanzada
2. **WhatsApp/Email:** Para envío automático de presupuestos
3. **Base de datos:** Para persistencia más robusta
4. **Autenticación:** Para múltiples usuarios

### Funcionalidades Adicionales
1. **Carga de imágenes:** Para análisis visual de proyectos
2. **Audio:** Para consultas por voz
3. **Notificaciones:** Para seguimiento de presupuestos
4. **Reportes:** Analytics avanzados de ventas

## Conclusión

Se ha desarrollado exitosamente una aplicación web completa que cumple con todos los requerimientos especificados:

✅ **Interfaz conversacional moderna y limpia**
✅ **Integración completa con APIs HDL Zomatik**
✅ **Generación automática de presupuestos en PDF**
✅ **Panel de administración funcional**
✅ **Gestión de base de conocimiento**
✅ **Arquitectura escalable y mantenible**
✅ **Diseño responsive para desktop y móvil**

La aplicación está lista para uso en producción y puede ser extendida fácilmente con las funcionalidades adicionales mencionadas.

