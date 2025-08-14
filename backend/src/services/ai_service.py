import os
import json
from typing import Dict, List, Optional, Any

from openai import OpenAI
from src.services.hdl_api import HDLApiService


SYSTEM_PROMPT = (
    "Eres un asistente interno de Corralón HDL que ayuda a operadores a armar presupuestos "
    "a partir de pedidos que llegan por WhatsApp. Responde de forma concisa, profesional y operativa. "
    "No inventes precios ni códigos: cuando sea necesario, sugiere usar las herramientas del sistema para "
    "buscar artículos o precios. Mantén un tono colaborativo, con foco en completar la información mínima "
    "(cliente, obra, lista de precios, cantidades y materiales)."
)


class AIService:
    """Servicio de IA con OpenAI para respuestas naturales y estructuradas."""
    
    def __init__(self):
        api_key = os.getenv("OPEN_AI_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta OPEN_AI_KEY/OPENAI_API_KEY en el entorno")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.hdl_service = HDLApiService()
        
    def process_message(self, message: str, conversation_history: List[Dict], files: Optional[List[Dict]] = None) -> Dict:
        """
        Procesa el mensaje con un modelo de lenguaje. Devuelve un dict con:
        - response: texto de respuesta
        - quick_replies: lista de sugerencias (opcional)
        - next_step: sugerencia de próximo paso (opcional)
        - needs_product_search: bool indicando si conviene buscar productos
        """
        history_messages = []
        for turn in conversation_history[-10:]:
            # Limitar historial a las últimas 10 entradas para evitar prompts enormes
            role = "user" if turn.get("role") == "user" else "assistant"
            content = str(turn.get("content", ""))[:4000]
            if content:
                history_messages.append({"role": role, "content": content})

        user_content = message.strip()[:6000]

        schema_instructions = (
            "Responde SOLO en JSON estricto con las claves: "
            "response (string), quick_replies (array de strings), next_step (string), "
            "needs_product_search (boolean), client_search_term (string|null). "
            "Si el usuario pide buscar un cliente/obra (ej. 'Walter'), establece client_search_term al término de búsqueda. "
            "Ejemplo: {\"response\":\"...\",\"quick_replies\":[\"...\"],\"next_step\":\"...\",\"needs_product_search\":false,\"client_search_term\":null}"
        )

        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT + " " + schema_instructions}]
            + history_messages
            + [{"role": "user", "content": user_content}]
        )

        completion = self.client.chat.completions.create(
            model=self.model,
                messages=messages,
            temperature=0.2,
        )

        text = completion.choices[0].message.content or "{}"
        try:
            data = json.loads(text)
        except Exception:
            # Fallback mínimo a formato esperado
            data = {
                "response": text.strip(),
                "quick_replies": [],
                "next_step": "continue_conversation",
                "needs_product_search": False,
            }

        # Garantizar claves
        data.setdefault("response", "")
        data.setdefault("quick_replies", [])
        data.setdefault("next_step", "continue_conversation")
        data.setdefault("needs_product_search", False)
        data.setdefault("client_search_term", None)

        # Heurística: si la IA no marcó client_search_term, intentar inferirlo del mensaje
        if not data.get("client_search_term"):
            ml = message.lower()
            # patrones simples: "busca a <nombre>", "buscar a <nombre>", "busca <nombre>"
            import re
            m = re.search(r"\bbusc(?:a|ar)\s+a\s+([a-záéíóúñü\-\s]{2,})", ml)
            if not m:
                m = re.search(r"\bbusc(?:a|ar)\s+([a-záéíóúñü\-]{3,})", ml)
            if m:
                term = m.group(1).strip()
                # limpiar posibles sufijos comunes
                term = term.split(" en ")[0].split(" del ")[0].split(" de ")[0].strip()
                # limitar longitud
                term = term[:50]
                if term:
                    data["client_search_term"] = term

        # Fallback de quick replies útiles si la IA no las entrega
        if not data.get("quick_replies"):
            data["quick_replies"] = [
                "Agregar obra",
                "Agregar lista de precios",
                "Agregar materiales y cantidades",
                "Buscar en el sistema",
                "Proporcionar más información",
            ]

        return data

    def search_products(self, query: str) -> List[Dict]:
        try:
            return self.hdl_service.search_articulos(query)
        except Exception:
            return []
    
    def analyze_image(self, image_base64: str) -> Dict[str, Any]:
        """Analiza una imagen con un prompt de clasificación simple."""
        try:
            # Usamos multimodal si el modelo lo soporta; para simplicidad, devolvemos texto clasificado
            messages = [
                {"role": "system", "content": "Extrae materiales y señales útiles de la imagen. Responde en JSON con 'analysis' y 'materials_detected'"},
                    {
                        "role": "user",
                        "content": [
                        {"type": "input_text", "text": "Analiza la imagen y sugiere categorías de materiales"},
                        {"type": "input_image", "image_data": image_base64},
                    ],
                },
            ]
            completion = self.client.chat.completions.create(model=self.model, messages=messages, temperature=0)
            text = completion.choices[0].message.content or "{}"
            return json.loads(text)
        except Exception:
            return {"analysis": "Imagen recibida.", "materials_detected": []}

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """Transcribe audio si está disponible; si no, devuelve cadena vacía."""
        try:
            # Implementación simple omitida por ahora para no bloquear; se puede integrar whisper/gpt-4o-transcribe
            return ""
        except Exception:
            return ""
    
    def generate_budget_summary(self, items: List[Dict]) -> Dict:
        total = sum(item.get("total", 0) for item in items)
        prompt = (
            "Genera un breve resumen ejecutivo del presupuesto en 3-5 líneas. "
            "No inventes materiales ni precios. Solo resume cantidades y total. "
            f"Total: {total:.2f}. Formato JSON: {{\"summary\": string, \"total_amount\": number, \"item_count\": number}}"
        )
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            text = completion.choices[0].message.content or "{}"
            data = json.loads(text)
            data.setdefault("total_amount", total)
            data.setdefault("item_count", len(items))
            return data
        except Exception:
            return {"summary": "", "total_amount": total, "item_count": len(items)}

