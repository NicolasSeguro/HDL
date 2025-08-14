import json
import random
from typing import Dict, List, Optional, Any
from src.services.hdl_api import HDLApiService

class SimpleAIService:
    """Servicio de IA simplificado para desarrollo sin dependencias externas"""
    
    def __init__(self):
        self.hdl_service = HDLApiService()
        
        # Respuestas predefinidas para diferentes tipos de consultas
        self.responses = {
            'greeting': [
                "¡Hola! Perfecto, estoy aquí para ayudarte con tu presupuesto de materiales de construcción.",
                "¡Excelente! Vamos a trabajar juntos en tu presupuesto. ¿Podrías contarme más detalles sobre tu proyecto?"
            ],
            'cement': [
                "Perfecto, tenemos varios tipos de cemento disponibles. ¿Para qué tipo de obra lo necesitas?",
                "Excelente elección. El cemento es fundamental en cualquier construcción. ¿Cuántos metros cuadrados vas a construir?"
            ],
            'house': [
                "Una casa de 120m² es un proyecto interesante. ¿En qué etapa de la obra estás? ¿Estructura, terminaciones o obra completa?",
                "Para una casa de esas dimensiones necesitaremos calcular varios materiales. ¿Tienes los planos o especificaciones técnicas?"
            ],
            'materials': [
                "Te voy a mostrar algunos materiales que podrían interesarte para tu proyecto.",
                "Basándome en tu consulta, he encontrado estos productos en nuestro catálogo."
            ],
            'default': [
                "Entiendo tu consulta. Para poder ayudarte mejor, ¿podrías darme más detalles sobre tu proyecto?",
                "Perfecto, estoy analizando tu solicitud. ¿Qué tipo de obra estás planificando?"
            ]
        }
        
        # Respuestas rápidas según el contexto
        self.quick_replies = {
            'project_type': ["Casa particular", "Edificio", "Reforma", "Obra comercial"],
            'construction_stage': ["Estructura", "Terminaciones", "Obra completa"],
            'area_size': ["50m²", "100m²", "150m²", "200m²", "Otro"],
            'confirm': ["Sí, correcto", "No, modificar", "Agregar más"]
        }
    
    def process_message(self, message: str, conversation_history: List[Dict], 
                       files: Optional[List[Dict]] = None) -> Dict:
        """
        Procesa un mensaje del usuario y genera una respuesta
        """
        try:
            message_lower = message.lower()
            
            # Determinar el tipo de consulta
            response_type = self._classify_message(message_lower)
            
            # Generar respuesta
            response_text = random.choice(self.responses[response_type])
            
            # Determinar respuestas rápidas
            quick_replies = self._get_quick_replies(message_lower, response_type)
            
            # Buscar productos si es relevante
            needs_search = self._needs_product_search(message_lower)
            
            result = {
                "response": response_text,
                "needs_product_search": needs_search,
                "quick_replies": quick_replies,
                "next_step": self._determine_next_step(message_lower, response_type)
            }
            
            return result
            
        except Exception as e:
            return {
                "response": f"Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.",
                "needs_product_search": False,
                "quick_replies": [],
                "next_step": "error"
            }
    
    def search_products(self, query: str) -> List[Dict]:
        """
        Busca productos en el catálogo HDL
        """
        try:
            return self.hdl_service.search_articulos(query)
        except Exception as e:
            return []
    
    def analyze_image(self, image_data: str) -> Dict:
        """
        Analiza una imagen (versión simplificada)
        """
        return {
            "analysis": "He recibido tu imagen. Basándome en lo que puedo ver, parece ser relacionado con construcción. ¿Podrías describir qué materiales específicos necesitas?",
            "materials_detected": ["cemento", "ladrillo", "arena"]
        }
    
    def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio (versión simplificada)
        """
        return "Audio recibido. Por favor, escribe tu consulta en el chat para poder ayudarte mejor."
    
    def generate_budget_summary(self, items: List[Dict]) -> Dict:
        """
        Genera un resumen del presupuesto
        """
        try:
            total = sum(item.get('total', 0) for item in items)
            
            summary = f"""
Resumen del Presupuesto:

Total de items: {len(items)}
Monto total: ${total:,.2f}

Este presupuesto incluye los materiales básicos para tu proyecto de construcción.
Te recomiendo revisar las cantidades y consultar con un profesional para validar
que sean suficientes para tu obra específica.
            """.strip()
            
            return {
                "summary": summary,
                "total_amount": total,
                "item_count": len(items),
                "categories": self._categorize_items(items)
            }
            
        except Exception as e:
            return {
                "summary": f"Error al generar resumen: {str(e)}",
                "total_amount": 0,
                "item_count": 0,
                "categories": []
            }
    
    def _classify_message(self, message: str) -> str:
        """
        Clasifica el tipo de mensaje para generar una respuesta apropiada
        """
        if any(word in message for word in ['hola', 'buenos', 'buenas', 'saludos']):
            return 'greeting'
        elif any(word in message for word in ['cemento', 'cal', 'yeso']):
            return 'cement'
        elif any(word in message for word in ['casa', 'vivienda', 'm2', 'metros']):
            return 'house'
        elif any(word in message for word in ['material', 'producto', 'articulo', 'precio']):
            return 'materials'
        else:
            return 'default'
    
    def _get_quick_replies(self, message: str, response_type: str) -> List[str]:
        """
        Genera respuestas rápidas basadas en el contexto
        """
        if response_type == 'house' or 'tipo de obra' in message:
            return self.quick_replies['project_type']
        elif 'etapa' in message or 'fase' in message:
            return self.quick_replies['construction_stage']
        elif 'metros' in message or 'superficie' in message:
            return self.quick_replies['area_size']
        elif 'confirmar' in message or 'correcto' in message:
            return self.quick_replies['confirm']
        else:
            return []
    
    def _needs_product_search(self, message: str) -> bool:
        """
        Determina si se necesita buscar productos
        """
        search_keywords = [
            'cemento', 'cal', 'yeso', 'ladrillo', 'bloque', 'arena',
            'piedra', 'adhesivo', 'klaukol', 'material', 'producto',
            'precio', 'costo', 'cuanto', 'disponible'
        ]
        
        return any(keyword in message for keyword in search_keywords)
    
    def _determine_next_step(self, message: str, response_type: str) -> str:
        """
        Determina el siguiente paso en el flujo de conversación
        """
        if 'presupuesto' in message and ('listo' in message or 'final' in message):
            return "generate_budget"
        elif self._needs_product_search(message):
            return "search_products"
        elif 'confirmar' in message or 'correcto' in message:
            return "confirm_details"
        else:
            return "continue_conversation"
    
    def _categorize_items(self, items: List[Dict]) -> List[Dict]:
        """
        Categoriza los items del presupuesto
        """
        categories = {}
        
        for item in items:
            nombre = item.get('nombre', '').lower()
            
            if any(word in nombre for word in ['cemento', 'cal', 'yeso']):
                category = 'Morteros y Aglomerantes'
            elif any(word in nombre for word in ['ladrillo', 'bloque']):
                category = 'Mampostería'
            elif any(word in nombre for word in ['piedra', 'arena']):
                category = 'Áridos'
            elif any(word in nombre for word in ['klaukol', 'adhesivo']):
                category = 'Adhesivos'
            else:
                category = 'Otros'
            
            if category not in categories:
                categories[category] = {'items': 0, 'total': 0}
            
            categories[category]['items'] += 1
            categories[category]['total'] += item.get('total', 0)
        
        return [{'name': k, **v} for k, v in categories.items()]

