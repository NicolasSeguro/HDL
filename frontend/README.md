# Asistente de Presupuestos - Frontend

Aplicación React para el asistente inteligente de presupuestos de corralón HDL.

## Características

- 🎨 Interfaz moderna con shadcn/ui y Tailwind CSS
- 💬 Chat conversacional inteligente
- 📊 Panel de administración completo
- 📱 Diseño responsive para desktop y móvil
- 🔄 Navegación fluida entre secciones

## Tecnologías

- **React 18** - Framework principal
- **Vite** - Build tool y dev server
- **shadcn/ui** - Componentes UI
- **Tailwind CSS** - Estilos
- **Lucide React** - Iconos

## Instalación

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Iniciar servidor de desarrollo:**
   ```bash
   npm run dev
   ```

3. **Abrir en navegador:**
   ```
   http://localhost:5173
   ```

## Estructura del Proyecto

```
src/
├── components/
│   ├── ChatInterface.jsx      # Interfaz principal de chat
│   ├── AdminPanel.jsx         # Panel de administración
│   └── ui/                    # Componentes UI (shadcn/ui)
├── services/
│   └── api.js                 # Cliente API para backend
├── App.jsx                    # Componente principal
└── main.jsx                   # Punto de entrada
```

## Componentes Principales

### ChatInterface
- Interfaz de chat conversacional
- Manejo de mensajes y respuestas
- Integración con backend para IA
- Botones de respuesta rápida

### AdminPanel
- Dashboard con estadísticas
- Gestión de presupuestos
- Base de conocimiento
- Búsqueda y filtros

## Configuración del Backend

Asegúrate de que el backend esté ejecutándose en `http://localhost:5000` antes de usar la aplicación.

## Scripts Disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Build para producción
- `npm run preview` - Preview del build
- `npm run lint` - Linter ESLint

## Deployment

Para deployment en producción, usar:

```bash
npm run build
```

Los archivos se generarán en la carpeta `dist/`.

## Personalización

### Colores
Los colores principales se pueden modificar en `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#1e40af',    // Azul principal
      secondary: '#374151',  // Gris oscuro
      accent: '#059669',     // Verde para totales
    }
  }
}
```

### Componentes UI
Los componentes de shadcn/ui se pueden personalizar en `src/components/ui/`.

## Funcionalidades

### Chat
- Envío de mensajes de texto
- Respuestas automáticas del bot
- Botones de respuesta rápida
- Historial de conversación

### Administración
- Estadísticas de presupuestos
- Listado de presupuestos históricos
- Gestión de base de conocimiento
- Búsqueda avanzada

## Integración con Backend

La aplicación se comunica con el backend a través de:

- `POST /api/chat/message` - Enviar mensajes
- `GET /api/budget/list` - Listar presupuestos
- `POST /api/knowledge/add` - Agregar conocimiento
- Y más endpoints documentados en el backend

## Troubleshooting

### Error de CORS
Si hay errores de CORS, verificar que el backend tenga CORS habilitado para `http://localhost:5173`.

### Backend no disponible
Verificar que el backend esté ejecutándose en el puerto 5000:
```bash
curl http://localhost:5000/
```

### Dependencias
Si hay problemas con dependencias, limpiar e instalar:
```bash
rm -rf node_modules package-lock.json
npm install
```

