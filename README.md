# Business Analytics Dashboard - Análisis de KPIs

Proyecto de análisis de negocio para cálculo y visualización de KPIs críticos como NPS, CSAT, tasa de conversión y métricas de ventas. Preparado para integración con herramientas de BI como Tableau, Power BI y Looker Studio.

## Descripción

Este proyecto implementa un sistema de análisis de métricas de negocio que:
- Calcula KPIs clave (NPS, CSAT, conversión, ventas)
- Analiza el ciclo de vida del producto
- Genera datos estructurados para dashboards
- Prepara exportaciones para Tableau, Power BI y otras herramientas

Desarrollado para demostrar competencias en análisis de negocio y visualización de datos.

## Tecnologías

- Python 3.8+
- Pandas - análisis y manipulación de datos
- NumPy - cálculos numéricos

## Estructura del Proyecto

```
business-analytics-dashboard/
│
├── data_analyzer.py        # Analizador principal de KPIs
├── dashboard_generator.py   # Generador de datos para dashboards
├── requirements.txt         # Dependencias
└── README.md               # Documentación
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/JosefaOgalde/business-analytics-dashboard.git
cd business-analytics-dashboard

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Análisis de KPIs

```python
from data_analyzer import BusinessAnalytics

# Crear analizador
analyzer = BusinessAnalytics()

# Cargar datos
analyzer.load_data('data/sample_business_data.csv')

# Calcular KPIs
analyzer.calculate_nps()
analyzer.calculate_csat()
analyzer.calculate_conversion_rate()
analyzer.calculate_sales_metrics()

# Generar reporte
print(analyzer.get_summary_report())

# Exportar para dashboard
analyzer.export_to_json('dashboard_data.json')
```

### Generar datos para dashboards

```python
from dashboard_generator import DashboardGenerator
import json

# Cargar datos de KPIs
with open('dashboard_data.json', 'r') as f:
    kpis_data = json.load(f)['kpis']

# Generar archivos para diferentes herramientas
generator = DashboardGenerator(kpis_data)
generator.prepare_tableau_data()      # CSV para Tableau
generator.prepare_powerbi_data()     # JSON para Power BI
generator.generate_summary_table()    # Tabla resumen
```

## KPIs Calculados

### NPS (Net Promoter Score)
- Clasificación de promotores, pasivos y detractores
- Cálculo del score NPS
- Porcentajes por categoría

### CSAT (Customer Satisfaction)
- Score de satisfacción del cliente
- Porcentaje de clientes satisfechos
- Promedio de satisfacción

### Tasa de Conversión
- Conversiones vs visitantes
- Porcentaje de conversión
- Métricas de rendimiento

### Métricas de Ventas
- Ventas totales
- Promedio y mediana
- Crecimiento temporal

## Integración con Herramientas de BI

### Tableau
Los datos se exportan en formato CSV listo para importar en Tableau.

### Power BI
Se genera un archivo JSON estructurado compatible con Power BI.

### Looker Studio / Big Query
Los datos pueden exportarse directamente o conectarse vía API.

## Ejecutar Análisis Completo

```bash
python data_analyzer.py
```

Esto generará:
- Datos de ejemplo
- Cálculo de todos los KPIs
- Reporte resumen
- Archivo JSON para dashboards

## Autor

Josefa Ogalde - Ingeniera en Informática

---

*Proyecto desarrollado para demostrar competencias en análisis de negocio y visualización de datos.*
