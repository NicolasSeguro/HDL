import requests
import json
from typing import Dict, List, Optional
import time
import os
from src.services.mock_data import MOCK_SOCIEDADES, MOCK_CLIENTES_OBRAS, MOCK_ARTICULOS

class HDLApiService:
    """Servicio para integrar con las APIs de HDL Zomatik"""
    
    BASE_URL = os.getenv("HDL_API_BASE", "https://hdl.zomatik.com/ws_web.php")
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutos
        # Desactivar mocks por defecto. Activar explícitamente con USE_MOCK_DATA=true si se desea.
        self.use_mock = os.getenv('USE_MOCK_DATA', 'false').lower() == 'true'
    
    def _get_cached_data(self, key: str) -> Optional[Dict]:
        """Obtiene datos del cache si están disponibles y no han expirado"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
        return None
    
    def _set_cache_data(self, key: str, data: Dict):
        """Guarda datos en el cache"""
        self.cache[key] = (data, time.time())
    
    def _make_request(self, operacion: int) -> Dict:
        """Realiza una petición a la API de HDL o devuelve datos de prueba"""
        cache_key = f"operacion_{operacion}"
        
        # Verificar cache primero
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Usar datos de prueba si está habilitado
        if self.use_mock:
            if operacion == 1:
                data = MOCK_CLIENTES_OBRAS
            elif operacion == 2:
                data = MOCK_SOCIEDADES
            elif operacion == 3:
                data = MOCK_ARTICULOS
            else:
                data = {"resultado": 0, "error": "Operación no válida"}
            
            self._set_cache_data(cache_key, data)
            return data
        
        try:
            response = requests.get(
                self.BASE_URL,
                params={'operacion': operacion},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Guardar en cache
            self._set_cache_data(cache_key, data)
            
            return data
        except requests.exceptions.RequestException as e:
            # Fallback a datos de prueba si falla la API
            print(f"API request failed, using mock data: {str(e)}")
            if operacion == 1:
                data = MOCK_CLIENTES_OBRAS
            elif operacion == 2:
                data = MOCK_SOCIEDADES
            elif operacion == 3:
                data = MOCK_ARTICULOS
            else:
                data = {"resultado": 0, "error": "Operación no válida"}
            
            self._set_cache_data(cache_key, data)
            return data
        except json.JSONDecodeError as e:
            raise Exception(f"Error al decodificar respuesta JSON: {str(e)}")
    
    def get_clientes_y_obras(self) -> Dict:
        """
        Operación 1: Obtiene información de clientes, sociedades y obras
        """
        return self._make_request(1)

    def search_clientes(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Busca clientes y/o obras por término. Coincide por razón social, CUIT o nombre de obra.
        Devuelve una lista simplificada: [{ razon_social, cuit, obras: [{codigo, nombre, listas: [...] }] }]
        """
        try:
            data = self.get_clientes_y_obras()
            clientes = data.get('clientes', [])
            query_lower = (query or '').lower().strip()
            results: List[Dict] = []

            for cliente in clientes:
                if len(results) >= limit:
                    break

                datos = cliente.get('datos', {})
                razon = (datos.get('razon_social') or '').lower()
                cuit = (datos.get('cuit') or '').lower()
                obras = cliente.get('obras', [])

                # Coincidencia por cliente
                cliente_match = (query_lower in razon) or (query_lower and query_lower in cuit)

                # Filtrar obras coincidentes por nombre
                obras_match = []
                for obra in obras:
                    nombre_obra = (obra.get('nombre') or '').lower()
                    if query_lower in nombre_obra or cliente_match:
                        obras_match.append({
                            'codigo': obra.get('codigo'),
                            'nombre': obra.get('nombre'),
                            'listas': obra.get('listas', [])
                        })

                if cliente_match or obras_match:
                    results.append({
                        'razon_social': datos.get('razon_social'),
                        'cuit': datos.get('cuit'),
                        'obras': obras_match
                    })

            return results
        except Exception as e:
            raise Exception(f"Error al buscar clientes: {str(e)}")
    
    def get_sucursales_y_sociedades(self) -> Dict:
        """
        Operación 2: Obtiene información de sucursales y sociedades
        """
        return self._make_request(2)
    
    def get_articulos_y_precios(self) -> Dict:
        """
        Operación 3: Obtiene el catálogo completo de artículos y precios
        """
        return self._make_request(3)
    
    def search_articulos(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Busca artículos por nombre o código
        """
        try:
            data = self.get_articulos_y_precios()
            articulos = data.get('articulos', [])
            
            query_lower = query.lower()
            results = []
            
            for articulo in articulos:
                if len(results) >= limit:
                    break
                
                nombre = articulo.get('nombre', '').lower()
                codigo = articulo.get('codigo', '').lower()
                
                if query_lower in nombre or query_lower in codigo:
                    results.append(articulo)
            
            return results
        except Exception as e:
            raise Exception(f"Error al buscar artículos: {str(e)}")
    
    def get_articulo_by_codigo(self, codigo: str) -> Optional[Dict]:
        """
        Obtiene un artículo específico por su código
        """
        try:
            data = self.get_articulos_y_precios()
            articulos = data.get('articulos', [])
            
            for articulo in articulos:
                if articulo.get('codigo') == codigo:
                    return articulo
            
            return None
        except Exception as e:
            raise Exception(f"Error al obtener artículo: {str(e)}")
    
    def get_listas_precios_by_obra(self, codigo_obra: str) -> List[Dict]:
        """
        Obtiene las listas de precios disponibles para una obra específica
        """
        try:
            data = self.get_clientes_y_obras()
            clientes = data.get('clientes', [])
            
            for cliente in clientes:
                obras = cliente.get('obras', [])
                for obra in obras:
                    if obra.get('codigo') == codigo_obra:
                        return obra.get('listas', [])
            
            return []
        except Exception as e:
            raise Exception(f"Error al obtener listas de precios: {str(e)}")
    
    def get_precio_articulo(self, codigo_articulo: str, codigo_lista: str) -> Optional[float]:
        """
        Obtiene el precio de un artículo en una lista específica
        """
        try:
            articulo = self.get_articulo_by_codigo(codigo_articulo)
            if not articulo:
                return None
            
            precios = articulo.get('precios', [])
            for precio in precios:
                if precio.get('codigo') == codigo_lista:
                    precio_str = precio.get('precio', '0')
                    return float(precio_str)
            
            return None
        except Exception as e:
            raise Exception(f"Error al obtener precio: {str(e)}")
    
    def get_sociedades(self) -> List[Dict]:
        """
        Obtiene la lista de sociedades disponibles
        """
        try:
            data = self.get_sucursales_y_sociedades()
            return data.get('sociedades', [])
        except Exception as e:
            raise Exception(f"Error al obtener sociedades: {str(e)}")
    
    def clear_cache(self):
        """Limpia el cache"""
        self.cache.clear()

