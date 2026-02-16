"""
Generador de dashboards para visualización de KPIs
Prepara datos para Tableau, Power BI, Looker Studio
"""

import pandas as pd
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardGenerator:
    """Genera datos estructurados para dashboards"""
    
    def __init__(self, kpis_data):
        """
        Inicializa el generador de dashboards.
        
        Args:
            kpis_data: Diccionario con datos de KPIs
        """
        self.kpis_data = kpis_data
    
    def prepare_tableau_data(self, output_path='tableau_data.csv'):
        """
        Prepara datos en formato para Tableau
        """
        logger.info("Preparando datos para Tableau...")
        
        # Crear DataFrame con métricas
        metrics = []
        
        if 'nps' in self.kpis_data:
            metrics.append({
                'Metrica': 'NPS',
                'Valor': self.kpis_data['nps']['valor'],
                'Categoria': 'Satisfacción',
                'Fecha': datetime.now().strftime('%Y-%m-%d')
            })
        
        if 'csat' in self.kpis_data:
            metrics.append({
                'Metrica': 'CSAT',
                'Valor': self.kpis_data['csat']['valor'],
                'Categoria': 'Satisfacción',
                'Fecha': datetime.now().strftime('%Y-%m-%d')
            })
        
        if 'conversion_rate' in self.kpis_data:
            metrics.append({
                'Metrica': 'Tasa de Conversión',
                'Valor': self.kpis_data['conversion_rate']['valor'],
                'Categoria': 'Rendimiento',
                'Fecha': datetime.now().strftime('%Y-%m-%d')
            })
        
        if 'sales' in self.kpis_data:
            metrics.append({
                'Metrica': 'Ventas Totales',
                'Valor': self.kpis_data['sales']['total'],
                'Categoria': 'Ventas',
                'Fecha': datetime.now().strftime('%Y-%m-%d')
            })
        
        df = pd.DataFrame(metrics)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        logger.info(f"Datos para Tableau guardados en: {output_path}")
        return output_path
    
    def prepare_powerbi_data(self, output_path='powerbi_data.json'):
        """
        Prepara datos en formato JSON para Power BI
        """
        logger.info("Preparando datos para Power BI...")
        
        powerbi_format = {
            'timestamp': datetime.now().isoformat(),
            'metrics': []
        }
        
        for kpi_name, kpi_data in self.kpis_data.items():
            if isinstance(kpi_data, dict) and 'valor' in kpi_data:
                powerbi_format['metrics'].append({
                    'name': kpi_name.upper(),
                    'value': kpi_data['valor'],
                    'details': kpi_data
                })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(powerbi_format, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Datos para Power BI guardados en: {output_path}")
        return output_path
    
    def generate_summary_table(self, output_path='kpis_summary.csv'):
        """
        Genera tabla resumen de KPIs para cualquier herramienta
        """
        logger.info("Generando tabla resumen de KPIs...")
        
        summary = []
        
        for kpi_name, kpi_data in self.kpis_data.items():
            if isinstance(kpi_data, dict):
                row = {'KPI': kpi_name.upper()}
                
                if 'valor' in kpi_data:
                    row['Valor'] = kpi_data['valor']
                
                # Agregar otros campos relevantes
                for key, value in kpi_data.items():
                    if key != 'valor' and not isinstance(value, (dict, list)):
                        row[key.capitalize()] = value
                
                summary.append(row)
        
        df = pd.DataFrame(summary)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        logger.info(f"Tabla resumen guardada en: {output_path}")
        return output_path


def main():
    """Ejemplo de uso"""
    # Cargar datos de ejemplo
    with open('dashboard_data.json', 'r', encoding='utf-8') as f:
        kpis_data = json.load(f)['kpis']
    
    # Crear generador
    generator = DashboardGenerator(kpis_data)
    
    # Generar archivos para diferentes herramientas
    generator.prepare_tableau_data()
    generator.prepare_powerbi_data()
    generator.generate_summary_table()
    
    print("\nArchivos generados:")
    print("- tableau_data.csv (para Tableau)")
    print("- powerbi_data.json (para Power BI)")
    print("- kpis_summary.csv (tabla resumen)")


if __name__ == "__main__":
    main()
