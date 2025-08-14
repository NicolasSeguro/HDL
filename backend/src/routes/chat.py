from flask import Blueprint, request, jsonify
from src.services.ai_service import AIService
from src.services.hdl_api import HDLApiService
import base64
import json
import time

chat_bp = Blueprint('chat', __name__)
ai_service = AIService()
hdl_service = HDLApiService()

@chat_bp.route('/message', methods=['POST'])
def process_message():
    """
    Procesa un mensaje del usuario y devuelve la respuesta del asistente
    """
    try:
        data = request.get_json()
        
        message = data.get('message', '')
        conversation_history = data.get('history', [])
        files = data.get('files', [])
        
        if not message and not files:
            return jsonify({
                'error': 'Mensaje o archivos requeridos'
            }), 400
        
        # Procesar archivos si los hay
        processed_files = []
        for file_data in files:
            if file_data.get('type') == 'image':
                # El archivo ya viene en base64 desde el frontend
                processed_files.append({
                    'type': 'image',
                    'data': file_data.get('data')
                })
            elif file_data.get('type') == 'audio':
                # Transcribir audio
                audio_bytes = base64.b64decode(file_data.get('data'))
                transcription = ai_service.transcribe_audio(audio_bytes)
                message += f" [Audio transcrito: {transcription}]"
        
        # Procesar mensaje con IA
        result = ai_service.process_message(message, conversation_history, processed_files)
        
        # Buscar productos si es necesario
        products = []
        if result.get('needs_product_search'):
            products = ai_service.search_products(message)

        # Búsqueda de clientes/obras si el modelo lo sugiere
        clients = []
        client_search_term = result.get('client_search_term')
        if not client_search_term:
            # Inferir término desde el mensaje si el modelo no lo dio
            try:
                msg_lower = (message or '').lower()
                import re
                m = re.search(r"\bbusc(?:a|ar)\s+a\s+([a-záéíóúñü\-\s]{2,})", msg_lower)
                if not m:
                    m = re.search(r"\bbusc(?:a|ar)\s+([a-záéíóúñü\-]{3,})", msg_lower)
                if m:
                    client_search_term = m.group(1).strip().split(' en ')[0][:50]
            except Exception:
                client_search_term = None

        if client_search_term:
            clients = hdl_service.search_clientes(client_search_term, limit=20)
        
        return jsonify({
            'response': result['response'],
            'quick_replies': result.get('quick_replies', []),
            'next_step': result.get('next_step', 'continue'),
            'products': products[:10],  # Limitar a 10 productos
            'clients': clients[:10],    # Limitar a 10 clientes/obras
            'timestamp': data.get('timestamp')
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al procesar mensaje: {str(e)}'
        }), 500

@chat_bp.route('/search-products', methods=['POST'])
def search_products():
    """
    Busca productos en el catálogo HDL
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        limit = data.get('limit', 50)
        
        if not query:
            return jsonify({
                'error': 'Query de búsqueda requerido'
            }), 400
        
        products = hdl_service.search_articulos(query, limit)
        
        return jsonify({
            'products': products,
            'total': len(products)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al buscar productos: {str(e)}'
        }), 500


@chat_bp.route('/search-clients', methods=['POST'])
def search_clients():
    """
    Busca clientes y/o obras por término (razón social, CUIT o nombre de obra)
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        limit = data.get('limit', 50)

        if not query:
            return jsonify({'error': 'Query de búsqueda requerido'}), 400

        clients = hdl_service.search_clientes(query, limit)
        return jsonify({'clients': clients, 'total': len(clients)})
    except Exception as e:
        return jsonify({'error': f'Error al buscar clientes: {str(e)}'}), 500

@chat_bp.route('/product/<codigo>', methods=['GET'])
def get_product(codigo):
    """
    Obtiene información detallada de un producto
    """
    try:
        product = hdl_service.get_articulo_by_codigo(codigo)
        
        if not product:
            return jsonify({
                'error': 'Producto no encontrado'
            }), 404
        
        return jsonify({
            'product': product
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener producto: {str(e)}'
        }), 500

@chat_bp.route('/societies', methods=['GET'])
def get_societies():
    """
    Obtiene la lista de sociedades disponibles
    """
    try:
        societies = hdl_service.get_sociedades()
        
        return jsonify({
            'societies': societies
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener sociedades: {str(e)}'
        }), 500

@chat_bp.route('/price-lists/<codigo_obra>', methods=['GET'])
def get_price_lists(codigo_obra):
    """
    Obtiene las listas de precios para una obra específica
    """
    try:
        price_lists = hdl_service.get_listas_precios_by_obra(codigo_obra)
        
        return jsonify({
            'price_lists': price_lists
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener listas de precios: {str(e)}'
        }), 500

@chat_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    """
    Analiza una imagen para extraer información relevante
    """
    try:
        data = request.get_json()
        image_data = data.get('image_data', '')
        
        if not image_data:
            return jsonify({
                'error': 'Datos de imagen requeridos'
            }), 400
        
        # Remover el prefijo data:image si existe
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        result = ai_service.analyze_image(image_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Error al analizar imagen: {str(e)}'
        }), 500

@chat_bp.route('/generate-budget', methods=['POST'])
def generate_budget():
    """
    Genera un presupuesto basado en los items seleccionados
    """
    try:
        data = request.get_json()
        items = data.get('items', [])
        client_info = data.get('client_info', {})
        
        if not items:
            return jsonify({
                'error': 'Items requeridos para generar presupuesto'
            }), 400
        
        # Generar resumen con IA
        summary = ai_service.generate_budget_summary(items)
        
        # Calcular totales
        subtotal = sum(item.get('total', 0) for item in items)
        iva = subtotal * 0.21  # IVA 21%
        total = subtotal + iva
        
        budget = {
            'id': f"PRES-{int(time.time())}",
            'client_info': client_info,
            'items': items,
            'subtotal': subtotal,
            'iva': iva,
            'total': total,
            'summary': summary,
            'created_at': time.time()
        }
        
        return jsonify({
            'budget': budget
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar presupuesto: {str(e)}'
        }), 500

@chat_bp.route('/clear-cache', methods=['POST'])
def clear_cache():
    """
    Limpia el cache de las APIs
    """
    try:
        hdl_service.clear_cache()
        
        return jsonify({
            'message': 'Cache limpiado exitosamente'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al limpiar cache: {str(e)}'
        }), 500

