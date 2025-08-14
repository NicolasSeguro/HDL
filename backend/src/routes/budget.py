from flask import Blueprint, request, jsonify, send_file
from src.services.pdf_service import PDFService
from src.services.simple_ai_service import SimpleAIService
import os
import tempfile
from datetime import datetime
import json

budget_bp = Blueprint('budget', __name__)
pdf_service = PDFService()
ai_service = SimpleAIService()

@budget_bp.route('/generate', methods=['POST'])
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
                'error': 'No se proporcionaron items para el presupuesto'
            }), 400
        
        # Calcular totales
        subtotal = sum(item.get('total', 0) for item in items)
        iva = subtotal * 0.21
        total = subtotal + iva
        
        # Generar resumen con IA
        summary = ai_service.generate_budget_summary(items)
        
        # Crear el presupuesto
        budget = {
            'id': f"PRES-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'client_info': client_info,
            'items': items,
            'subtotal': subtotal,
            'iva': iva,
            'total': total,
            'summary': summary
        }
        
        return jsonify({
            'budget': budget,
            'message': 'Presupuesto generado exitosamente'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar presupuesto: {str(e)}'
        }), 500

@budget_bp.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Genera un PDF del presupuesto
    """
    try:
        data = request.get_json()
        budget_data = data.get('budget')
        
        if not budget_data:
            return jsonify({
                'error': 'No se proporcionaron datos del presupuesto'
            }), 400
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name
        
        # Generar PDF
        pdf_service.generate_budget_pdf(budget_data, pdf_path)
        
        # Enviar archivo
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"presupuesto_{budget_data.get('id', 'HDL')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar PDF: {str(e)}'
        }), 500

@budget_bp.route('/quick-pdf', methods=['POST'])
def generate_quick_pdf():
    """
    Genera un PDF rápido con items básicos
    """
    try:
        data = request.get_json()
        items = data.get('items', [])
        client_name = data.get('client_name', '')
        
        if not items:
            return jsonify({
                'error': 'No se proporcionaron items para el presupuesto'
            }), 400
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name
        
        # Generar PDF simple
        pdf_service.generate_simple_budget_pdf(items, client_name, pdf_path)
        
        # Enviar archivo
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"presupuesto_rapido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar PDF rápido: {str(e)}'
        }), 500

@budget_bp.route('/save', methods=['POST'])
def save_budget():
    """
    Guarda un presupuesto en el sistema
    """
    try:
        data = request.get_json()
        budget = data.get('budget')
        
        if not budget:
            return jsonify({
                'error': 'No se proporcionaron datos del presupuesto'
            }), 400
        
        # Crear directorio de presupuestos si no existe
        budgets_dir = '/tmp/budgets'
        os.makedirs(budgets_dir, exist_ok=True)
        
        # Guardar presupuesto como JSON
        budget_id = budget.get('id', f"PRES-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        budget_file = os.path.join(budgets_dir, f"{budget_id}.json")
        
        with open(budget_file, 'w', encoding='utf-8') as f:
            json.dump(budget, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'message': 'Presupuesto guardado exitosamente',
            'budget_id': budget_id,
            'file_path': budget_file
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al guardar presupuesto: {str(e)}'
        }), 500

@budget_bp.route('/list', methods=['GET'])
def list_budgets():
    """
    Lista todos los presupuestos guardados
    """
    try:
        budgets_dir = '/tmp/budgets'
        
        if not os.path.exists(budgets_dir):
            return jsonify({'budgets': []})
        
        budgets = []
        for filename in os.listdir(budgets_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(budgets_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        budget = json.load(f)
                        budgets.append({
                            'id': budget.get('id'),
                            'created_at': budget.get('created_at'),
                            'client_name': budget.get('client_info', {}).get('name', 'Sin nombre'),
                            'total': budget.get('total', 0),
                            'items_count': len(budget.get('items', []))
                        })
                except Exception:
                    continue
        
        # Ordenar por fecha de creación (más recientes primero)
        budgets.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({'budgets': budgets})
        
    except Exception as e:
        return jsonify({
            'error': f'Error al listar presupuestos: {str(e)}'
        }), 500

@budget_bp.route('/<budget_id>', methods=['GET'])
def get_budget(budget_id):
    """
    Obtiene un presupuesto específico
    """
    try:
        budgets_dir = '/tmp/budgets'
        budget_file = os.path.join(budgets_dir, f"{budget_id}.json")
        
        if not os.path.exists(budget_file):
            return jsonify({
                'error': 'Presupuesto no encontrado'
            }), 404
        
        with open(budget_file, 'r', encoding='utf-8') as f:
            budget = json.load(f)
        
        return jsonify({'budget': budget})
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener presupuesto: {str(e)}'
        }), 500

