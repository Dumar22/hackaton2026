"""
Exportador de datos a múltiples formatos: CSV, Excel, SQL, PDF, JSON
"""
import csv
import json
import io
from typing import List, Dict, BinaryIO
from datetime import datetime
import os

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class DataExporter:
    """Exporta datos a múltiples formatos"""
    
    def __init__(self, data: List[Dict], headers: List[str] = None):
        """
        Args:
            data: Lista de diccionarios con los datos
            headers: Lista de nombres de columnas (opcional)
        """
        self.data = data
        self.headers = headers or (list(data[0].keys()) if data else [])
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def to_csv(self, filepath: str = None) -> str:
        """
        Exporta a CSV
        
        Args:
            filepath: Ruta del archivo (si no se proporciona, genera automática)
        
        Returns:
            Ruta del archivo creado
        """
        if not filepath:
            filepath = f"export_{self.timestamp}.csv"
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.data)
        
        return filepath
    
    def to_json(self, filepath: str = None) -> str:
        """
        Exporta a JSON
        
        Args:
            filepath: Ruta del archivo (si no se proporciona, genera automática)
        
        Returns:
            Ruta del archivo creado
        """
        if not filepath:
            filepath = f"export_{self.timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def to_sql(self, table_name: str = "datos", filepath: str = None) -> str:
        """
        Exporta a SQL INSERT statements
        
        Args:
            table_name: Nombre de la tabla
            filepath: Ruta del archivo (si no se proporciona, genera automática)
        
        Returns:
            Ruta del archivo creado
        """
        if not filepath:
            filepath = f"export_{self.timestamp}.sql"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Crear tabla
            f.write(f"-- Crear tabla\n")
            f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
            
            for i, field in enumerate(self.headers):
                f.write(f"    {field.lower().replace(' ', '_')} VARCHAR(255)")
                if i < len(self.headers) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            
            f.write(");\n\n")
            
            # Insertar datos
            f.write(f"-- Insertar {len(self.data)} registros\n")
            for record in self.data:
                columns = ', '.join([k.lower().replace(' ', '_') for k in self.headers])
                values_list = []
                for v in record.values():
                    escaped = str(v).replace("'", "''")
                    values_list.append(f"'{escaped}'")
                values = ', '.join(values_list)
                f.write(f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n")
        
        return filepath
    
    def to_excel(self, filepath: str = None) -> str:
        """
        Exporta a Excel (requiere pandas y openpyxl)
        
        Args:
            filepath: Ruta del archivo (si no se proporciona, genera automática)
        
        Returns:
            Ruta del archivo creado
        """
        if not PANDAS_AVAILABLE:
            raise ImportError("Se requiere 'pandas' para exportar a Excel")
        
        if not filepath:
            filepath = f"export_{self.timestamp}.xlsx"
        
        df = pd.DataFrame(self.data)
        df.to_excel(filepath, index=False, sheet_name='Datos')
        
        return filepath
    
    def to_pdf(self, filepath: str = None, max_rows: int = 100) -> str:
        """
        Exporta a PDF (requiere reportlab)
        Nota: Los PDFs grandes con muchas filas pueden ser lentos
        
        Args:
            filepath: Ruta del archivo (si no se proporciona, genera automática)
            max_rows: Máximo número de filas a mostrar
        
        Returns:
            Ruta del archivo creado
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError("Se requiere 'reportlab' para exportar a PDF")
        
        if not filepath:
            filepath = f"export_{self.timestamp}.pdf"
        
        # Limitar filas para PDF
        data_to_export = self.data[:max_rows]
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor='darkblue',
            spaceAfter=20
        )
        elements.append(Paragraph('Reporte de Datos', title))
        elements.append(Spacer(1, 0.2*inch))
        
        # Información
        info = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=10,
            textColor='gray'
        )
        elements.append(Paragraph(
            f'Total de registros: {len(self.data)} | Mostrando: {len(data_to_export)}',
            info
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Tabla
        table_data = [self.headers]
        for row in data_to_export:
            table_data.append([str(row.get(h, '')) for h in self.headers])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#4472C4'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#F0F0F0'),
            ('GRID', (0, 0), (-1, -1), 1, '#CCCCCC'),
        ]))
        
        elements.append(table)
        
        doc.build(elements)
        
        return filepath
    
    def export_all(self, output_dir: str = "./exports") -> Dict[str, str]:
        """
        Exporta a todos los formatos disponibles
        
        Args:
            output_dir: Directorio de salida
        
        Returns:
            Diccionario con rutas de archivos generados
        """
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        
        # CSV
        try:
            csv_path = self.to_csv(f"{output_dir}/export_{self.timestamp}.csv")
            results['csv'] = csv_path
        except Exception as e:
            results['csv_error'] = str(e)
        
        # JSON
        try:
            json_path = self.to_json(f"{output_dir}/export_{self.timestamp}.json")
            results['json'] = json_path
        except Exception as e:
            results['json_error'] = str(e)
        
        # SQL
        try:
            sql_path = self.to_sql(filepath=f"{output_dir}/export_{self.timestamp}.sql")
            results['sql'] = sql_path
        except Exception as e:
            results['sql_error'] = str(e)
        
        # Excel
        try:
            if PANDAS_AVAILABLE:
                excel_path = self.to_excel(f"{output_dir}/export_{self.timestamp}.xlsx")
                results['excel'] = excel_path
            else:
                results['excel_warning'] = 'pandas no instalado'
        except Exception as e:
            results['excel_error'] = str(e)
        
        # PDF
        try:
            if REPORTLAB_AVAILABLE:
                pdf_path = self.to_pdf(f"{output_dir}/export_{self.timestamp}.pdf")
                results['pdf'] = pdf_path
            else:
                results['pdf_warning'] = 'reportlab no instalado'
        except Exception as e:
            results['pdf_error'] = str(e)
        
        return results
