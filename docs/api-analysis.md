# Análisis de API HDL Zomatik

## URL 1: Operación 1 - Obras y Listas de Precios
**URL:** https://hdl.zomatik.com/ws_web.php?operacion=1

### Estructura del JSON:
- **resultado**: 1 (indica éxito)
- **clientes**: Array de clientes

### Estructura de cada cliente:
- **datos**: Información básica del cliente
  - email
  - cuit
  - telefono
  - razon_social
- **sociedades**: Array de sociedades asociadas
  - codigo
  - nombre
- **obras**: Array de obras del cliente
  - codigo
  - nombre
  - **listas**: Array de listas de precios para cada obra
    - nombre (ID numérico)
    - codigo (descripción de la lista)

### Ejemplos encontrados:

#### Cliente 1: Walter SA
- **CUIT:** 20316528210
- **Email:** zechner.walter@gmail.com
- **Sociedades:** 5 sociedades (Prueba, Materiales y Logistica SRL, HDL Distribuidora SRL, DLM Construccion SRL, SYL Materiales Urbanos S.R.L.)
- **Obras:** 5 obras (Helguera 225, Helguera 333, Helguera 2206, OBRA PARPAT, Eitan Casa)

#### Cliente 2: EITAN SOBOL
- **CUIT:** 11111158
- **Sociedades:** 2 sociedades (HDL URBANA S.R.L., Prueba)
- **Obras:** 2 obras (Los cardales Country Club LOTE 612, Rawson 152)

### Tipos de listas de precios identificadas:
- Lista Obra C12 (14462)
- Lista Obra C20 (13186)
- Lista Obra base (14458)
- Lista Acopio C12-12 new (14409)
- Lista reventa C12-12 (14431)
- Lista reventa C12-12-6 (14432)



## URL 2: Operación 2 - Sucursales y Sociedades
**URL:** https://hdl.zomatik.com/ws_web.php?operacion=2

### Estructura del JSON:
- **resultado**: 1 (indica éxito)
- **sociedades**: Array de sociedades

### Estructura de cada sociedad:
- **nombre**: Nombre de la sociedad
- **codigo**: Código identificador de la sociedad
- **sucursales**: Array de sucursales de la sociedad
  - **nombre**: Nombre de la sucursal
  - **codigo**: Código identificador de la sucursal

### Sociedades encontradas:

1. **DLM Construccion SRL** (Código: 15)
   - Sucursal: DLM (Código: 17)

2. **Prueba** (Código: 18)
   - Sucursal: Prueba (Código: 18)

3. **Materiales y Logistica SRL** (Código: 17)
   - Sucursal: MyL (Código: 20)

4. **HDL URBANA S.R.L.** (Código: 22)
   - Sucursal: HDL URBANA (Código: 29)

### Observaciones:
- Cada sociedad tiene al menos una sucursal
- Los códigos de sociedades y sucursales son únicos
- Algunas sociedades tienen el mismo nombre que sus sucursales (ej: "Prueba")


## URL 3: Operación 3 - Artículos y Precios
**URL:** https://hdl.zomatik.com/ws_web.php?operacion=3

### Estructura del JSON:
- **resultado**: 1 (indica éxito)
- **articulos**: Array extenso de artículos (miles de productos)

### Estructura de cada artículo:
- **codigo**: Código identificador del artículo
- **nombre**: Descripción del producto
- **codigoint**: Código interno del artículo
- **precios**: Array de precios según diferentes listas
  - **codigo**: Código de la lista de precios
  - **nombre**: Nombre descriptivo de la lista
  - **precio**: Precio del artículo en esa lista (formato decimal como string)

### Ejemplos de artículos encontrados:

#### Materiales de Construcción:
1. **PIEDRA PARTIDA (6a20) X M3 CAMION** (Código: 10104)
   - Lista Obra Mercado Libre: $79,794.368

2. **PIEDRA PARTIDA (6a20) X M3** (Código: 10120)
   - Lista reventa C12-CANUELAS: $71,066.667

3. **ARENA X M3 CAMION** (Código: 10118)
   - Lista Obra Mercado Libre: $37,696.117

4. **LADRILLO COMUN** (Código: 30101)
   - Lista Obra Mercado Libre: $192.391

5. **LADRILLO COMUN 1\\/2 VISTA** (Código: 30102)
   - Lista Obra Mercado Libre: $3.195

6. **LADRILLO HUECO 8X18X33** (Código: 30104)
   - Lista Obra Mercado Libre: $579.870

7. **LADRILLO HUECO 12X18X33 (9a)** (Código: 30106)
   - Lista Obra Mercado Libre: $719.060

8. **LADRILLO HUECO 18X18X33 (12a)** (Código: 30107)
   - Lista Obra Mercado Libre: $1,027.032

9. **LADRILLO PORTANTE 12X19X33** (Código: 30108)
   - Lista Obra Mercado Libre: $1,257.140

10. **LADRILLO PORTANTE 18X19X33** (Código: 30109)
    - Lista Obra Mercado Libre: $1,567.819

11. **WEBER SUPER PINGUINO BLANCO X 25 KG** (Código: 50103)
    - Lista Obra Mercado Libre: $52,972.656

12. **CAL MILAGRO X 25 KG (CEFAS)** (Código: 50108)
    - Lista Obra Mercado Libre: $16,808.684

13. **YESO ALPRESS x 35 KG** (Código: 50115)
    - Lista Obra Mercado Libre: $15,087.668

14. **CAL HIDRAT EXTRA AVELLANEDA X 25 KG** (Código: 50206)
    - Lista Obra Mercado Libre: $4,978.877

15. **KLAUKOL PASTINA PERFORMANCE MUSGO X 5 KG** (Código: 50216)
    - Lista Obra Mercado Libre: $25,723.420

### Observaciones importantes:
- El catálogo es muy extenso (más de 238,000 píxeles de contenido)
- Incluye materiales de construcción diversos: piedra, arena, ladrillos, cal, yeso, adhesivos, etc.
- Los precios están en formato decimal como strings
- Cada artículo puede tener múltiples listas de precios
- La lista "Lista Obra Mercado Libre" (código 14473) aparece frecuentemente
- Los precios varían significativamente según el tipo de producto


## Resumen y Análisis Completo

### Arquitectura del Sistema HDL Zomatik

El sistema HDL Zomatik presenta una arquitectura de API bien estructurada que maneja tres aspectos fundamentales del negocio de materiales de construcción:

1. **Gestión de Clientes y Obras** (operacion=1)
2. **Estructura Organizacional** (operacion=2) 
3. **Catálogo de Productos y Precios** (operacion=3)

### Relaciones entre las APIs

#### Códigos de Sociedades:
Las sociedades aparecen en múltiples endpoints:
- **Operación 1**: Sociedades asociadas a clientes
- **Operación 2**: Detalle completo de sociedades y sucursales

**Sociedades identificadas:**
- SYL Materiales Urbanos S.R.L. (Código: 1)
- DLM Construccion SRL (Código: 15)
- HDL Distribuidora SRL (Código: 16)
- Materiales y Logistica SRL (Código: 17)
- Prueba (Código: 18)
- HDL URBANA S.R.L. (Código: 22)

#### Códigos de Listas de Precios:
Las listas de precios conectan las obras con los artículos:

**Listas identificadas:**
- 13186: Lista Obra C20
- 14409: Lista Acopio C12-12 new
- 14431: Lista reventa C12-12
- 14432: Lista reventa C12-12-6
- 14455: Lista reventa C12-CANUELAS
- 14458: Lista Obra base
- 14462: Lista Obra C12
- 14473: Lista Obra Mercado Libre

### Modelo de Negocio Identificado

#### Estructura Jerárquica:
1. **Sociedades** → **Sucursales**
2. **Clientes** → **Obras** → **Listas de Precios**
3. **Artículos** → **Precios por Lista**

#### Tipos de Listas de Precios:
- **Listas de Obra**: Precios específicos para proyectos (C12, C20, base)
- **Listas de Reventa**: Precios para distribuidores
- **Listas de Acopio**: Precios para almacenamiento
- **Lista Mercado Libre**: Precios para venta online

### Características del Catálogo

#### Categorías de Productos:
- **Áridos**: Piedra partida, arena
- **Mampostería**: Ladrillos comunes, huecos, portantes
- **Morteros y Adhesivos**: Weber, Klaukol
- **Materiales Básicos**: Cal, yeso

#### Rangos de Precios (Lista Mercado Libre):
- **Productos básicos**: $3 - $200 (ladrillos individuales)
- **Materiales por bolsa**: $4,000 - $26,000 (25-35 kg)
- **Materiales por m³**: $37,000 - $80,000 (áridos)

### Conclusiones Técnicas

#### Fortalezas del Sistema:
1. **Estructura JSON consistente** en las tres operaciones
2. **Códigos únicos** para identificación de entidades
3. **Flexibilidad en precios** por obra y tipo de cliente
4. **Catálogo extenso** con miles de productos

#### Consideraciones de Implementación:
1. **Volumen de datos**: La operación 3 maneja un catálogo muy extenso
2. **Formato de precios**: Los precios están como strings decimales
3. **Relaciones complejas**: Múltiples niveles de jerarquía organizacional
4. **Gestión de listas**: Sistema sofisticado de precios diferenciados

### Casos de Uso Identificados:
1. **Consulta de precios por obra específica**
2. **Gestión de catálogo por sociedad/sucursal**
3. **Comparación de precios entre listas**
4. **Administración de clientes y proyectos**

