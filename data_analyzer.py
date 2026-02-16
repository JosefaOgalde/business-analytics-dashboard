"""
Analizador de datos de negocio
Análisis de KPIs y métricas de producto digital
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BusinessAnalytics:
    """Clase para análisis de métricas de negocio y KPIs"""
    
    def __init__(self, data_path=None):
        """
        Inicializa el analizador de negocio.
        
        Args:
            data_path: Ruta al archivo de datos (opcional)
        """
        self.data = None
        self.kpis = {}
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path):
        """Carga datos desde archivo CSV o Excel"""
        logger.info(f"Cargando datos desde: {data_path}")
        try:
            if data_path.endswith('.csv'):
                self.data = pd.read_csv(data_path, encoding='utf-8')
            elif data_path.endswith(('.xlsx', 'xls')):
                self.data = pd.read_excel(data_path)
            else:
                raise ValueError("Formato no soportado. Use CSV o Excel")
            
            logger.info(f"Datos cargados: {len(self.data)} registros, {len(self.data.columns)} columnas")
            return self.data
        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise
    
    def calculate_nps(self, nps_column='nps_score'):
        """
        Calcula el Net Promoter Score (NPS)
        NPS = % Promotores - % Detractores
        """
        if self.data is None or nps_column not in self.data.columns:
            logger.warning(f"Columna {nps_column} no encontrada")
            return None
        
        scores = self.data[nps_column].dropna()
        
        promotores = (scores >= 9).sum()
        pasivos = ((scores >= 7) & (scores <= 8)).sum()
        detractores = (scores <= 6).sum()
        total = len(scores)
        
        if total == 0:
            return None
        
        pct_promotores = (promotores / total) * 100
        pct_detractores = (detractores / total) * 100
        nps = pct_promotores - pct_detractores
        
        self.kpis['nps'] = {
            'valor': round(nps, 2),
            'promotores': promotores,
            'pasivos': pasivos,
            'detractores': detractores,
            'total_respuestas': total,
            'pct_promotores': round(pct_promotores, 2),
            'pct_detractores': round(pct_detractores, 2)
        }
        
        logger.info(f"NPS calculado: {nps:.2f}")
        return nps
    
    def calculate_csat(self, csat_column='satisfaction_score'):
        """
        Calcula el Customer Satisfaction Score (CSAT)
        CSAT = (Clientes satisfechos / Total respuestas) * 100
        """
        if self.data is None or csat_column not in self.data.columns:
            logger.warning(f"Columna {csat_column} no encontrada")
            return None
        
        scores = self.data[csat_column].dropna()
        satisfechos = (scores >= 4).sum()  # Asumiendo escala 1-5
        total = len(scores)
        
        if total == 0:
            return None
        
        csat = (satisfechos / total) * 100
        
        self.kpis['csat'] = {
            'valor': round(csat, 2),
            'satisfechos': satisfechos,
            'total_respuestas': total,
            'promedio': round(scores.mean(), 2)
        }
        
        logger.info(f"CSAT calculado: {csat:.2f}%")
        return csat
    
    def calculate_conversion_rate(self, conversions_column='converted', visitors_column='visitors'):
        """
        Calcula la tasa de conversión
        Tasa de conversión = (Conversiones / Visitantes) * 100
        """
        if self.data is None:
            return None
        
        # Si hay columnas específicas
        if conversions_column in self.data.columns and visitors_column in self.data.columns:
            conversions = self.data[conversions_column].sum()
            visitors = self.data[visitors_column].sum()
        else:
            # Calcular desde datos agregados
            if 'conversion' in self.data.columns:
                conversions = (self.data['conversion'] == True).sum()
                visitors = len(self.data)
            else:
                logger.warning("No se encontraron columnas de conversión")
                return None
        
        if visitors == 0:
            return None
        
        conversion_rate = (conversions / visitors) * 100
        
        self.kpis['conversion_rate'] = {
            'valor': round(conversion_rate, 2),
            'conversiones': int(conversions),
            'visitantes': int(visitors)
        }
        
        logger.info(f"Tasa de conversión: {conversion_rate:.2f}%")
        return conversion_rate
    
    def calculate_sales_metrics(self, sales_column='sales', date_column='date'):
        """
        Calcula métricas de ventas
        """
        if self.data is None or sales_column not in self.data.columns:
            logger.warning(f"Columna {sales_column} no encontrada")
            return None
        
        sales = self.data[sales_column].dropna()
        
        total_sales = sales.sum()
        avg_sales = sales.mean()
        median_sales = sales.median()
        
        # Si hay columna de fecha, calcular tendencias
        if date_column in self.data.columns:
            self.data[date_column] = pd.to_datetime(self.data[date_column], errors='coerce')
            sales_by_date = self.data.groupby(self.data[date_column].dt.date)[sales_column].sum()
            
            # Crecimiento mes a mes (si hay suficientes datos)
            if len(sales_by_date) > 1:
                growth = ((sales_by_date.iloc[-1] - sales_by_date.iloc[0]) / sales_by_date.iloc[0]) * 100
            else:
                growth = 0
        else:
            growth = None
        
        self.kpis['sales'] = {
            'total': round(total_sales, 2),
            'promedio': round(avg_sales, 2),
            'mediana': round(median_sales, 2),
            'crecimiento': round(growth, 2) if growth else None
        }
        
        logger.info(f"Ventas totales: ${total_sales:,.2f}")
        return self.kpis['sales']
    
    def analyze_product_lifecycle(self, date_column='date', status_column='status'):
        """
        Analiza el ciclo de vida del producto
        """
        if self.data is None:
            return None
        
        analysis = {}
        
        # Análisis por estado si existe
        if status_column in self.data.columns:
            status_counts = self.data[status_column].value_counts()
            analysis['por_estado'] = status_counts.to_dict()
        
        # Análisis temporal si hay fecha
        if date_column in self.data.columns:
            self.data[date_column] = pd.to_datetime(self.data[date_column], errors='coerce')
            analysis['por_mes'] = self.data.groupby(self.data[date_column].dt.to_period('M')).size().to_dict()
            analysis['por_semana'] = self.data.groupby(self.data[date_column].dt.to_period('W')).size().to_dict()
        
        self.kpis['product_lifecycle'] = analysis
        logger.info("Análisis de ciclo de vida completado")
        return analysis
    
    def generate_dashboard_data(self):
        """
        Genera datos estructurados para dashboard
        """
        dashboard = {
            'fecha_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'kpis': self.kpis,
            'resumen': {
                'total_registros': len(self.data) if self.data is not None else 0,
                'columnas': list(self.data.columns) if self.data is not None else []
            }
        }
        
        return dashboard
    
    def export_to_json(self, output_path='dashboard_data.json'):
        """Exporta datos del dashboard a JSON"""
        dashboard_data = self.generate_dashboard_data()
        
        # Convertir Period objects a strings para JSON
        def convert_period(obj):
            if hasattr(obj, 'strftime'):
                return str(obj)
            elif isinstance(obj, dict):
                return {str(k): convert_period(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_period(item) for item in obj]
            return obj
        
        dashboard_data = convert_period(dashboard_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Datos exportados a: {output_path}")
        return output_path
    
    def get_summary_report(self):
        """Genera reporte resumen de KPIs"""
        report = "\n" + "=" * 60
        report += "\nREPORTE DE KPIs - BUSINESS ANALYTICS"
        report += "\n" + "=" * 60
        
        if 'nps' in self.kpis:
            nps_data = self.kpis['nps']
            report += f"\n\nNPS (Net Promoter Score): {nps_data['valor']}"
            report += f"\n  Promotores: {nps_data['promotores']} ({nps_data['pct_promotores']}%)"
            report += f"\n  Detractores: {nps_data['detractores']} ({nps_data['pct_detractores']}%)"
        
        if 'csat' in self.kpis:
            csat_data = self.kpis['csat']
            report += f"\n\nCSAT: {csat_data['valor']}%"
            report += f"\n  Satisfechos: {csat_data['satisfechos']}/{csat_data['total_respuestas']}"
        
        if 'conversion_rate' in self.kpis:
            conv_data = self.kpis['conversion_rate']
            report += f"\n\nTasa de Conversión: {conv_data['valor']}%"
            report += f"\n  Conversiones: {conv_data['conversiones']}"
            report += f"\n  Visitantes: {conv_data['visitantes']}"
        
        if 'sales' in self.kpis:
            sales_data = self.kpis['sales']
            report += f"\n\nVentas:"
            report += f"\n  Total: ${sales_data['total']:,.2f}"
            report += f"\n  Promedio: ${sales_data['promedio']:,.2f}"
            if sales_data['crecimiento']:
                report += f"\n  Crecimiento: {sales_data['crecimiento']:.2f}%"
        
        report += "\n" + "=" * 60
        
        return report


def main():
    """Función principal para ejecutar análisis"""
    # Crear instancia del analizador
    analyzer = BusinessAnalytics()
    
    # Ejemplo de uso con datos generados
    print("Generando datos de ejemplo...")
    
    # Generar datos de ejemplo
    np.random.seed(42)
    n_records = 1000
    
    data = {
        'date': pd.date_range(start='2024-01-01', periods=n_records, freq='D'),
        'nps_score': np.random.randint(0, 11, n_records),
        'satisfaction_score': np.random.randint(1, 6, n_records),
        'converted': np.random.choice([True, False], n_records, p=[0.15, 0.85]),
        'visitors': np.random.randint(100, 1000, n_records),
        'sales': np.random.normal(50000, 15000, n_records),
        'status': np.random.choice(['Activo', 'Inactivo', 'Nuevo'], n_records)
    }
    
    df = pd.DataFrame(data)
    df['sales'] = np.abs(df['sales'])  # Asegurar valores positivos
    
    # Guardar datos de ejemplo
    df.to_csv('data/sample_business_data.csv', index=False)
    print(f"Datos de ejemplo guardados: {len(df)} registros")
    
    # Cargar y analizar
    analyzer.load_data('data/sample_business_data.csv')
    
    # Calcular KPIs
    analyzer.calculate_nps()
    analyzer.calculate_csat()
    analyzer.calculate_conversion_rate()
    analyzer.calculate_sales_metrics()
    analyzer.analyze_product_lifecycle()
    
    # Generar reporte
    print(analyzer.get_summary_report())
    
    # Exportar datos para dashboard
    analyzer.export_to_json('dashboard_data.json')
    
    return analyzer


if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    main()
