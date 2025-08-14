# Arquitectura de la Aplicación - Asistente Inteligente para Presupuestos de Corralón

## Análisis de Requerimientos

### Funcionalidades Core
1. **Interfaz Conversacional Multimodal**
   - Input de texto, imagen, PDF y audio
   - Respuestas interactivas con botones de selección rápida
   - Edición de respuestas anteriores

2. **Generación de Presupuestos**
   - Vista previa editable
   - Exportación a PDF
   - Envío por email/WhatsApp

3. **Panel de Administración**
   - Histórico de presupuestos
   - Filtros por cliente, fecha, empresa
   - Gestión de conocimiento empresarial

4. **Integración con APIs HDL Zomatik**
   - Clientes y obras (operacion=1)
   - Sucursales y sociedades (operacion=2)
   - Catálogo de productos y precios (operacion=3)

## Análisis de Datos Empresariales

### Información de Materiales (Excel)
**Lista de Materiales (82 productos):**
- Cementos: Avellaneda, Hidralit
- Cales: Hidrat, Milagro
- Yesos: Tuyango, Alpress, Entre Ríos
- Ladrillos: Cerámicos, comunes, portantes, vista
- Adhesivos: Klaukol (múltiples tipos)
- Bloques: Retak (diferentes medidas)

**Capacidad de Flota:**
- Balancín: 10 posiciones, 20,000 kg
- Balancín Corto: 8 posiciones, 16,000 kg
- Chasis: 4 posiciones, 8,000 kg
- Semi: 16-30 posiciones, hasta 36,000 kg

### Integración con APIs HDL Zomatik

**Datos disponibles:**
- 6 sociedades principales
- Múltiples listas de precios diferenciadas
- Catálogo extenso (miles de productos)
- Precios por obra y tipo de cliente

## Arquitectura Técnica Propuesta

### Stack Tecnológico
- **Backend:** Flask (Python)
- **Frontend:** React
- **Base de Datos:** SQLite/PostgreSQL
- **IA:** OpenAI GPT-4 o Anthropic Claude
- **Procesamiento Multimodal:** OpenAI Vision, Whisper

### Estructura del Proyecto

```
presupuesto-assistant/
├── backend/
│   ├── app.py                 # Flask app principal
│   ├── models/               # Modelos de datos
│   ├── services/             # Servicios de negocio
│   │   ├── hdl_api.py       # Integración APIs HDL
│   │   ├── ai_service.py    # Servicio de IA
│   │   └── pdf_service.py   # Generación PDFs
│   ├── routes/              # Endpoints REST
│   └── utils/               # Utilidades
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/          # Páginas principales
│   │   ├── services/       # Servicios API
│   │   └── styles/         # Estilos CSS
│   └── public/
└── docs/                   # Documentación
```

### Componentes Principales

#### Backend Services

1. **HDL API Service**
   - Wrapper para las 3 operaciones de HDL Zomatik
   - Cache de datos para optimización
   - Manejo de errores y reintentos

2. **AI Service**
   - Integración con OpenAI/Anthropic
   - Procesamiento multimodal (texto, imagen, audio)
   - Contexto conversacional persistente

3. **PDF Service**
   - Generación de presupuestos en PDF
   - Templates personalizables
   - Integración con datos de empresa

#### Frontend Components

1. **ChatInterface**
   - Input multimodal
   - Historial de conversación
   - Botones de respuesta rápida

2. **BudgetPreview**
   - Vista previa editable
   - Cálculos automáticos
   - Validaciones

3. **AdminPanel**
   - Dashboard de presupuestos
   - Filtros y búsquedas
   - Gestión de conocimiento

### Base de Datos

```sql
-- Tablas principales
CREATE TABLE budgets (
    id INTEGER PRIMARY KEY,
    client_data JSON,
    items JSON,
    total_amount DECIMAL,
    status VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    budget_id INTEGER,
    messages JSON,
    context JSON,
    created_at TIMESTAMP
);

CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY,
    category VARCHAR(100),
    content TEXT,
    metadata JSON,
    created_at TIMESTAMP
);
```

## Flujo de Usuario

### 1. Inicio de Conversación
```
Usuario: "Necesito presupuesto para una casa de 120m2"
IA: "¡Perfecto! Para armar tu presupuesto necesito algunos datos:
    - ¿Para qué tipo de construcción? (Casa, edificio, reforma)
    - ¿Qué etapa de obra? (Estructura, terminaciones, completa)
    - ¿Tienes algún plano o lista de materiales?"
```

### 2. Recopilación de Información
- Selección de empresa/sucursal
- Identificación del cliente
- Análisis de archivos adjuntos
- Especificación de materiales

### 3. Generación de Presupuesto
- Búsqueda en catálogo HDL
- Aplicación de lista de precios correcta
- Cálculos de cantidades y totales
- Vista previa para edición

### 4. Finalización
- Generación de PDF
- Envío por email/WhatsApp
- Guardado en historial

## Consideraciones de Implementación

### Gestión de Conocimiento
- **Base de conocimiento empresarial:** Información sobre la empresa, políticas, procedimientos
- **Catálogo de materiales:** Integración con datos del Excel + APIs HDL
- **Experiencias previas:** Aprendizaje de presupuestos anteriores

### Optimizaciones
- **Cache de APIs:** Reducir llamadas a HDL Zomatik
- **Compresión de imágenes:** Para análisis más rápido
- **Respuestas streaming:** Para mejor UX en conversaciones largas

### Seguridad
- **Autenticación:** Para panel de admin
- **Validación de inputs:** Sanitización de archivos subidos
- **Rate limiting:** Para APIs externas

## Próximos Pasos

1. **Configuración del entorno de desarrollo**
2. **Implementación del backend básico**
3. **Integración con APIs HDL Zomatik**
4. **Desarrollo de la interfaz conversacional**
5. **Implementación de IA multimodal**
6. **Testing y refinamiento**
7. **Deployment y documentación**

