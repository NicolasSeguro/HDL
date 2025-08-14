from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime
from typing import Dict, List

class PDFService:
    """Servicio para generar PDFs de presupuestos"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para el título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e40af')
        )
        
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#374151')
        )
        
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Estilo para totales
        self.total_style = ParagraphStyle(
            'CustomTotal',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#059669'),
            alignment=TA_RIGHT
        )
    
    def generate_budget_pdf(self, budget_data: Dict, output_path: str) -> str:
        """
        Genera un PDF del presupuesto
        """
        try:
            # Crear el documento
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenido del PDF
            story = []
            
            # Encabezado
            self._add_header(story, budget_data)
            
            # Información del cliente
            self._add_client_info(story, budget_data.get('client_info', {}))
            
            # Tabla de productos
            self._add_products_table(story, budget_data.get('items', []))
            
            # Totales
            self._add_totals(story, budget_data)
            
            # Pie de página
            self._add_footer(story, budget_data)
            
            # Construir el PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error al generar PDF: {str(e)}")
    
    def _add_header(self, story: List, budget_data: Dict):
        """Agrega el encabezado del presupuesto"""
        # Título principal
        title = Paragraph("PRESUPUESTO DE MATERIALES", self.title_style)
        story.append(title)
        
        # Información de la empresa (desde variables de entorno)
        company_name = os.getenv('COMPANY_NAME', '')
        company_desc = os.getenv('COMPANY_DESC', '')
        company_phone = os.getenv('COMPANY_PHONE', '')
        company_info_text = "<br/>".join(filter(None, [
            f"<b>{company_name}</b>" if company_name else "",
            company_desc,
            f"Tel: {company_phone}" if company_phone else "",
        ]))
        company_info = Paragraph(company_info_text, self.normal_style)
        story.append(company_info)
        story.append(Spacer(1, 20))
        
        # Información del presupuesto
        budget_id = budget_data.get('id', 'N/A')
        created_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        budget_info = Paragraph(
            f"<b>Presupuesto N°:</b> {budget_id}<br/><b>Fecha:</b> {created_date}",
            self.normal_style
        )
        story.append(budget_info)
        story.append(Spacer(1, 20))
    
    def _add_client_info(self, story: List, client_info: Dict):
        """Agrega la información del cliente"""
        if not client_info:
            return
        
        story.append(Paragraph("DATOS DEL CLIENTE", self.subtitle_style))
        
        client_text = ""
        if client_info.get('name'):
            client_text += f"<b>Nombre:</b> {client_info['name']}<br/>"
        if client_info.get('email'):
            client_text += f"<b>Email:</b> {client_info['email']}<br/>"
        if client_info.get('phone'):
            client_text += f"<b>Teléfono:</b> {client_info['phone']}<br/>"
        if client_info.get('address'):
            client_text += f"<b>Dirección:</b> {client_info['address']}<br/>"
        
        if client_text:
            client_para = Paragraph(client_text, self.normal_style)
            story.append(client_para)
        
        story.append(Spacer(1, 20))
    
    def _add_products_table(self, story: List, items: List[Dict]):
        """Agrega la tabla de productos"""
        if not items:
            return
        
        story.append(Paragraph("DETALLE DE MATERIALES", self.subtitle_style))
        
        # Encabezados de la tabla
        data = [['Código', 'Descripción', 'Cantidad', 'Precio Unit.', 'Total']]
        
        # Agregar productos
        for item in items:
            codigo = item.get('codigo', 'N/A')
            nombre = item.get('nombre', 'Sin descripción')
            cantidad = item.get('cantidad', 1)
            precio_unit = item.get('precio_unitario', 0)
            total = item.get('total', 0)
            
            # Truncar nombre si es muy largo
            if len(nombre) > 40:
                nombre = nombre[:37] + "..."
            
            data.append([
                codigo,
                nombre,
                str(cantidad),
                f"${precio_unit:,.2f}",
                f"${total:,.2f}"
            ])
        
        # Crear la tabla
        table = Table(data, colWidths=[1*inch, 3*inch, 1*inch, 1.2*inch, 1.2*inch])
        
        # Estilo de la tabla
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Descripción alineada a la izquierda
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Números alineados a la derecha
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#374151')),
            
            # Alternar colores de filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    def _add_totals(self, story: List, budget_data: Dict):
        """Agrega los totales del presupuesto"""
        subtotal = budget_data.get('subtotal', 0)
        iva = budget_data.get('iva', 0)
        total = budget_data.get('total', 0)
        
        # Tabla de totales
        totals_data = [
            ['Subtotal:', f"${subtotal:,.2f}"],
            ['IVA (21%):', f"${iva:,.2f}"],
            ['TOTAL:', f"${total:,.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#059669')),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#059669')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 30))
    
    def _add_footer(self, story: List, budget_data: Dict):
        """Agrega el pie de página"""
        # Resumen de IA si está disponible
        summary = budget_data.get('summary', {})
        if summary and summary.get('summary'):
            story.append(Paragraph("OBSERVACIONES", self.subtitle_style))
            summary_text = summary['summary'].replace('\n', '<br/>')
            story.append(Paragraph(summary_text, self.normal_style))
            story.append(Spacer(1, 20))
        
        # Información adicional (desde variables de entorno)
        terms = os.getenv('PDF_TERMS', '')
        contact = os.getenv('PDF_CONTACT', '')
        footer_text = "<b>Condiciones:</b><br/>" + (terms.replace('\n', '<br/>') if terms else "") + "<br/><br/>" + contact.replace('\n', '<br/>')
        
        footer_para = Paragraph(footer_text, self.normal_style)
        story.append(footer_para)
    
    def generate_simple_budget_pdf(self, items: List[Dict], client_name: str = "", output_path: str = None) -> str:
        """
        Genera un PDF simple del presupuesto
        """
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"/tmp/presupuesto_{timestamp}.pdf"
        
        # Calcular totales
        subtotal = sum(item.get('total', 0) for item in items)
        iva = subtotal * 0.21
        total = subtotal + iva
        
        budget_data = {
            'id': f"PRES-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'client_info': {'name': client_name} if client_name else {},
            'items': items,
            'subtotal': subtotal,
            'iva': iva,
            'total': total
        }
        
        return self.generate_budget_pdf(budget_data, output_path)

