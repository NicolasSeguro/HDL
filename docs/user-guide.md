# Guía de Usuario - Asistente de Presupuestos HDL

Esta guía te ayudará a usar todas las funcionalidades del Asistente Inteligente de Presupuestos de Corralón HDL.

## 🚀 Acceso al Sistema

### URL de Acceso
- **Aplicación Principal:** http://localhost:5173 (desarrollo) o tu dominio en producción
- **API Backend:** http://localhost:5000 (desarrollo)

### Navegación Principal
La aplicación tiene dos secciones principales:
- **💬 Chat:** Para crear presupuestos de forma conversacional
- **🛠️ Administración:** Para gestionar presupuestos y conocimiento

## 💬 Usando el Chat Conversacional

### Inicio de Conversación
1. Al abrir la aplicación, verás un mensaje de bienvenida
2. Escribe tu consulta en el campo de texto inferior
3. Presiona Enter o haz clic en el botón de enviar

### Tipos de Consultas Soportadas

#### 🏗️ Consultas de Construcción
```
"Necesito materiales para construir una casa de 120m²"
"Quiero hacer una ampliación de 50m²"
"Necesito materiales para un muro de 20 metros"
```

#### 🧱 Consultas de Materiales Específicos
```
"Busco cemento Avellaneda"
"Necesito ladrillos comunes"
"Quiero cal hidratada"
"Busco adhesivo para cerámicos"
```

#### 💰 Consultas de Presupuestos
```
"Quiero un presupuesto para mi obra"
"¿Cuánto me sale construir un quincho?"
"Necesito precios de materiales básicos"
```

### Respuestas del Asistente
El asistente puede responder con:
- **Texto explicativo** sobre materiales o procesos
- **Botones de respuesta rápida** para agilizar la conversación
- **Lista de productos** del catálogo HDL
- **Preguntas de seguimiento** para entender mejor tu proyecto

### Botones de Respuesta Rápida
Cuando aparezcan, puedes hacer clic en:
- **Tipo de proyecto:** Casa particular, Edificio, Reforma, etc.
- **Etapa de obra:** Estructura, Terminaciones, Obra completa
- **Superficie:** 50m², 100m², 150m², etc.
- **Confirmaciones:** Sí correcto, No modificar, Agregar más

### Productos Mostrados
Cuando el asistente encuentra productos relevantes, verás:
- **Código del producto**
- **Nombre y descripción**
- **Precio unitario**
- **Botón para agregar al presupuesto**

## 📊 Generación de Presupuestos

### Proceso Automático
1. El asistente detecta cuando tienes suficiente información
2. Te pregunta si quieres generar el presupuesto
3. Confirma los datos del cliente (nombre, email, etc.)
4. Genera automáticamente el presupuesto

### Información Incluida
Cada presupuesto contiene:
- **Datos del cliente**
- **Lista detallada de materiales**
- **Cantidades y precios unitarios**
- **Subtotal, IVA (21%) y total**
- **Observaciones del asistente**
- **Condiciones comerciales**

### Formatos Disponibles
- **Vista en pantalla:** Para revisar antes de generar
- **PDF profesional:** Para descargar o enviar
- **Guardado automático:** En el historial del sistema

## 🛠️ Panel de Administración

### Acceso al Panel
1. Haz clic en "Administración" en el header superior
2. Verás el dashboard con estadísticas generales

### Dashboard Principal
El dashboard muestra:
- **📄 Total Presupuestos:** Cantidad de presupuestos generados
- **💰 Monto Total:** Suma de todos los presupuestos
- **📊 Promedio:** Monto promedio por presupuesto
- **📚 Base Conocimiento:** Cantidad de información almacenada

### Búsqueda Global
- Usa la barra de búsqueda superior para encontrar:
  - Presupuestos por cliente o ID
  - Información en la base de conocimiento
  - Productos específicos

## 📋 Gestión de Presupuestos

### Pestaña "Presupuestos"
Aquí puedes:
- **Ver historial completo** de presupuestos
- **Buscar por cliente** o fecha
- **Descargar PDFs** de presupuestos anteriores
- **Ver detalles** de cada presupuesto

### Información de Cada Presupuesto
- **ID único** del presupuesto
- **Nombre del cliente**
- **Fecha de creación**
- **Cantidad de items**
- **Monto total**
- **Botón de descarga PDF**

### Filtros y Búsqueda
- **Por cliente:** Escribe el nombre del cliente
- **Por fecha:** Usa el formato DD/MM/AAAA
- **Por monto:** Busca rangos específicos
- **Por ID:** Busca presupuestos específicos

## 📚 Base de Conocimiento

### Pestaña "Base de Conocimiento"
Esta sección permite gestionar la información que usa el asistente.

### Agregar Nuevo Conocimiento
1. **Título:** Nombre descriptivo de la información
2. **Categoría:** Selecciona el tipo:
   - **Información de Empresa:** Datos sobre HDL
   - **Productos y Materiales:** Especificaciones técnicas
   - **Políticas y Procedimientos:** Reglas de negocio
   - **Precios y Descuentos:** Información comercial
   - **Otros:** Información general
3. **Contenido:** Descripción detallada
4. **Guardar:** Haz clic en "Agregar Conocimiento"

### Gestión de Conocimiento Existente
Para cada item puedes:
- **Ver contenido completo**
- **Editar información** (botón de lápiz)
- **Eliminar** (botón de papelera)
- **Buscar** en títulos y contenido

### Categorías de Conocimiento

#### 🏢 Información de Empresa
- Historia y experiencia de HDL
- Horarios de atención
- Ubicaciones y sucursales
- Políticas generales

#### 🧱 Productos y Materiales
- Especificaciones técnicas
- Usos recomendados
- Marcas disponibles
- Características especiales

#### 📋 Políticas y Procedimientos
- Condiciones de venta
- Políticas de descuento
- Términos de entrega
- Garantías

#### 💰 Precios y Descuentos
- Descuentos por volumen
- Promociones especiales
- Condiciones de pago
- Precios especiales

## 🔍 Funciones de Búsqueda

### Búsqueda en Chat
- El asistente busca automáticamente productos relevantes
- Usa palabras clave como "cemento", "ladrillo", "cal"
- Muestra resultados del catálogo HDL en tiempo real

### Búsqueda en Administración
- **Global:** Busca en presupuestos y conocimiento
- **Por sección:** Usa las pestañas específicas
- **Filtros avanzados:** Combina criterios múltiples

### Consejos de Búsqueda
- Usa términos específicos: "cemento portland" vs "cemento"
- Combina palabras: "ladrillo común rojo"
- Usa códigos de producto si los conoces
- Prueba sinónimos: "cal" o "cal hidratada"

## 📱 Uso en Dispositivos Móviles

### Diseño Responsive
La aplicación se adapta automáticamente a:
- **📱 Teléfonos móviles**
- **📱 Tablets**
- **💻 Laptops**
- **🖥️ Monitores grandes**

### Funcionalidades Móviles
- **Chat táctil:** Teclado optimizado para móvil
- **Navegación por gestos:** Deslizar entre secciones
- **Botones grandes:** Fácil interacción táctil
- **Texto legible:** Tamaños optimizados

## 🎯 Consejos y Mejores Prácticas

### Para Obtener Mejores Resultados

#### 🗣️ En el Chat
- **Sé específico:** "Casa de 120m² con 3 dormitorios" vs "una casa"
- **Menciona la etapa:** "estructura", "terminaciones", "obra completa"
- **Indica cantidades:** "20 metros de muro", "100m² de losa"
- **Pregunta por alternativas:** "¿hay opciones más económicas?"

#### 📊 En Presupuestos
- **Revisa antes de generar:** Verifica cantidades y productos
- **Completa datos del cliente:** Facilita el seguimiento
- **Guarda información importante:** Usa la base de conocimiento
- **Descarga PDFs:** Para enviar por email o WhatsApp

#### 🛠️ En Administración
- **Mantén actualizada la base de conocimiento**
- **Revisa presupuestos regularmente**
- **Usa búsquedas para encontrar patrones**
- **Categoriza bien la información**

### Flujo de Trabajo Recomendado

#### Para Vendedores
1. **Recibir consulta del cliente**
2. **Usar el chat para entender necesidades**
3. **Generar presupuesto automáticamente**
4. **Revisar y ajustar si es necesario**
5. **Descargar PDF y enviar al cliente**
6. **Guardar en historial para seguimiento**

#### Para Administradores
1. **Revisar estadísticas diariamente**
2. **Actualizar base de conocimiento**
3. **Analizar presupuestos frecuentes**
4. **Optimizar información de productos**
5. **Capacitar al equipo en nuevas funciones**

## ❓ Preguntas Frecuentes

### ¿Cómo agrego un producto que no aparece?
El catálogo se actualiza automáticamente desde HDL. Si un producto no aparece, verifica:
- Que esté disponible en el sistema HDL
- Que uses el nombre correcto
- Que esté en la lista de precios activa

### ¿Puedo modificar un presupuesto después de generarlo?
Actualmente no se pueden modificar presupuestos generados. Puedes:
- Crear un nuevo presupuesto con los cambios
- Usar el chat para generar una versión actualizada
- Contactar al administrador para ajustes manuales

### ¿Los precios están actualizados?
Sí, los precios se obtienen en tiempo real desde las APIs de HDL Zomatik.

### ¿Puedo usar la aplicación sin internet?
No, la aplicación requiere conexión a internet para:
- Acceder al catálogo de productos
- Obtener precios actualizados
- Generar PDFs
- Sincronizar datos

### ¿Cómo exporto todos mis presupuestos?
Actualmente puedes descargar PDFs individuales. Para exportaciones masivas, contacta al administrador del sistema.

## 📞 Soporte y Contacto

### Soporte Técnico
- **Email:** soporte@hdl.com.ar
- **Teléfono:** (011) 4567-8900
- **Horario:** Lunes a Viernes 8:00 - 18:00

### Capacitación
- **Sesiones grupales:** Disponibles bajo solicitud
- **Manuales adicionales:** En la sección docs/
- **Videos tutoriales:** Próximamente disponibles

### Sugerencias y Mejoras
- **Email:** desarrollo@hdl.com.ar
- **Formulario:** Disponible en el panel de administración
- **Reuniones:** Mensuales para feedback

---

**¡Gracias por usar el Asistente de Presupuestos HDL!** 🏗️

