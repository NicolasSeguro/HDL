from flask import Blueprint, request, jsonify
import os
import json
from datetime import datetime

knowledge_bp = Blueprint('knowledge', __name__)

# Directorio para almacenar el conocimiento
KNOWLEDGE_DIR = '/tmp/knowledge'

def ensure_knowledge_dir():
    """Asegura que el directorio de conocimiento existe"""
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

@knowledge_bp.route('/list', methods=['GET'])
def list_knowledge():
    """
    Lista todo el conocimiento disponible
    """
    try:
        ensure_knowledge_dir()
        
        knowledge_items = []
        
        # Leer archivos de conocimiento
        for filename in os.listdir(KNOWLEDGE_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(KNOWLEDGE_DIR, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        item = json.load(f)
                        knowledge_items.append(item)
                except Exception:
                    continue
        
        # Ordenar por fecha de creación (más recientes primero)
        knowledge_items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({'knowledge': knowledge_items})
        
    except Exception as e:
        return jsonify({
            'error': f'Error al listar conocimiento: {str(e)}'
        }), 500

@knowledge_bp.route('/add', methods=['POST'])
def add_knowledge():
    """
    Agrega nuevo conocimiento a la base
    """
    try:
        data = request.get_json()
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', 'otros')
        
        if not title or not content:
            return jsonify({
                'error': 'Título y contenido son requeridos'
            }), 400
        
        ensure_knowledge_dir()
        
        # Crear el item de conocimiento
        knowledge_item = {
            'id': f"know_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'title': title,
            'content': content,
            'category': category,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Guardar en archivo
        filename = f"{knowledge_item['id']}.json"
        file_path = os.path.join(KNOWLEDGE_DIR, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_item, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'message': 'Conocimiento agregado exitosamente',
            'knowledge': knowledge_item
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al agregar conocimiento: {str(e)}'
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['GET'])
def get_knowledge(knowledge_id):
    """
    Obtiene un item específico de conocimiento
    """
    try:
        ensure_knowledge_dir()
        
        file_path = os.path.join(KNOWLEDGE_DIR, f"{knowledge_id}.json")
        
        if not os.path.exists(file_path):
            return jsonify({
                'error': 'Conocimiento no encontrado'
            }), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            knowledge_item = json.load(f)
        
        return jsonify({'knowledge': knowledge_item})
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener conocimiento: {str(e)}'
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['PUT'])
def update_knowledge(knowledge_id):
    """
    Actualiza un item de conocimiento
    """
    try:
        data = request.get_json()
        ensure_knowledge_dir()
        
        file_path = os.path.join(KNOWLEDGE_DIR, f"{knowledge_id}.json")
        
        if not os.path.exists(file_path):
            return jsonify({
                'error': 'Conocimiento no encontrado'
            }), 404
        
        # Leer el item existente
        with open(file_path, 'r', encoding='utf-8') as f:
            knowledge_item = json.load(f)
        
        # Actualizar campos
        if 'title' in data:
            knowledge_item['title'] = data['title'].strip()
        if 'content' in data:
            knowledge_item['content'] = data['content'].strip()
        if 'category' in data:
            knowledge_item['category'] = data['category']
        
        knowledge_item['updated_at'] = datetime.now().isoformat()
        
        # Guardar cambios
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_item, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'message': 'Conocimiento actualizado exitosamente',
            'knowledge': knowledge_item
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al actualizar conocimiento: {str(e)}'
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['DELETE'])
def delete_knowledge(knowledge_id):
    """
    Elimina un item de conocimiento
    """
    try:
        ensure_knowledge_dir()
        
        file_path = os.path.join(KNOWLEDGE_DIR, f"{knowledge_id}.json")
        
        if not os.path.exists(file_path):
            return jsonify({
                'error': 'Conocimiento no encontrado'
            }), 404
        
        os.remove(file_path)
        
        return jsonify({
            'message': 'Conocimiento eliminado exitosamente'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al eliminar conocimiento: {str(e)}'
        }), 500

@knowledge_bp.route('/search', methods=['POST'])
def search_knowledge():
    """
    Busca en la base de conocimiento
    """
    try:
        data = request.get_json()
        query = data.get('query', '').lower().strip()
        
        if not query:
            return jsonify({'results': []})
        
        ensure_knowledge_dir()
        
        results = []
        
        # Buscar en todos los archivos de conocimiento
        for filename in os.listdir(KNOWLEDGE_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(KNOWLEDGE_DIR, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        item = json.load(f)
                        
                        # Buscar en título y contenido
                        title_match = query in item.get('title', '').lower()
                        content_match = query in item.get('content', '').lower()
                        
                        if title_match or content_match:
                            # Calcular relevancia
                            relevance = 0
                            if title_match:
                                relevance += 2
                            if content_match:
                                relevance += 1
                            
                            item['relevance'] = relevance
                            results.append(item)
                            
                except Exception:
                    continue
        
        # Ordenar por relevancia
        results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({
            'error': f'Error al buscar conocimiento: {str(e)}'
        }), 500

@knowledge_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Obtiene las categorías disponibles
    """
    try:
        categories = [
            {'id': 'empresa', 'name': 'Información de Empresa'},
            {'id': 'productos', 'name': 'Productos y Materiales'},
            {'id': 'politicas', 'name': 'Políticas y Procedimientos'},
            {'id': 'precios', 'name': 'Precios y Descuentos'},
            {'id': 'otros', 'name': 'Otros'}
        ]
        
        return jsonify({'categories': categories})
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener categorías: {str(e)}'
        }), 500

@knowledge_bp.route('/export', methods=['GET'])
def export_knowledge():
    """
    Exporta toda la base de conocimiento
    """
    try:
        ensure_knowledge_dir()
        
        all_knowledge = []
        
        # Leer todos los archivos
        for filename in os.listdir(KNOWLEDGE_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(KNOWLEDGE_DIR, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        item = json.load(f)
                        all_knowledge.append(item)
                except Exception:
                    continue
        
        return jsonify({
            'knowledge_base': all_knowledge,
            'exported_at': datetime.now().isoformat(),
            'total_items': len(all_knowledge)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al exportar conocimiento: {str(e)}'
        }), 500

