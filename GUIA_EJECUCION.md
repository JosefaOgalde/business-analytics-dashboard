# Guía de Ejecución - Business Analytics Dashboard

Esta guía explica paso a paso cómo ejecutar el proyecto de análisis de KPIs.

## Requisitos Previos

- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)

## Paso 1: Navegar al directorio del proyecto

Abre una terminal (PowerShell, CMD, o Terminal de Cursor) y ve al directorio del proyecto:

```bash
cd C:\Users\josef\github\business-analytics-dashboard
```

## Paso 2: Instalar las dependencias

Instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

**Dependencias que se instalarán:**
- `pandas` - Para análisis y manipulación de datos
- `numpy` - Para cálculos numéricos
- `openpyxl` - Para leer archivos Excel

## Paso 3: Ejecutar el analizador de KPIs

Ejecuta el script principal que genera datos de ejemplo y calcula los KPIs:

```bash
python data_analyzer.py
```

**Esto realizará:**
1. Genera 1000 registros de datos de ejemplo
2. Calcula los KPIs principales:
   - **NPS** (Net Promoter Score)
   - **CSAT** (Customer Satisfaction)
   - **Tasa de Conversión**
   - **Métricas de Ventas**
3. Analiza el ciclo de vida del producto
4. Genera un reporte resumen en consola
5. Exporta datos a `dashboard_data.json`

**Salida esperada:**
```
Generando datos de ejemplo...
Datos de ejemplo guardados: 1000 registros

============================================================
REPORTE DE KPIs - BUSINESS ANALYTICS
============================================================

NPS (Net Promoter Score): -48.0
  Promotores: 171 (17.1%)
  Detractores: 651 (65.1%)

CSAT: 39.7%
  Satisfechos: 397/1000

Tasa de Conversión: 0.03%
  Conversiones: 157
  Visitantes: 546397

Ventas:
  Total: $50,111,275.32
  Promedio: $50,111.28
  Crecimiento: 108.16%
============================================================
```

## Paso 4: Generar archivos para dashboards

Ejecuta el generador de dashboards para crear archivos compatibles con diferentes herramientas de BI:

```bash
python dashboard_generator.py
```

**Esto generará:**
- `tableau_data.csv` - Datos formateados para Tableau
- `powerbi_data.json` - Datos en formato JSON para Power BI
- `kpis_summary.csv` - Tabla resumen de todos los KPIs

**Salida esperada:**
```
Preparando datos para Tableau...
Datos para Tableau guardados en: tableau_data.csv
Preparando datos para Power BI...
Datos para Power BI guardados en: powerbi_data.json
Generando tabla resumen de KPIs...
Tabla resumen guardada en: kpis_summary.csv

Archivos generados:
- tableau_data.csv (para Tableau)
- powerbi_data.json (para Power BI)
- kpis_summary.csv (tabla resumen)
```

## Paso 5: Verificar los archivos generados

Después de ejecutar ambos scripts, deberías tener los siguientes archivos:

```
business-analytics-dashboard/
│
├── data/
│   └── sample_business_data.csv    # Datos de ejemplo generados
│
├── dashboard_data.json              # Datos completos en JSON
├── tableau_data.csv                 # Para importar en Tableau
├── powerbi_data.json                # Para importar en Power BI
└── kpis_summary.csv                 # Tabla resumen
```

## Usar tus Propios Datos

Si quieres analizar tus propios datos:

1. **Prepara tu archivo CSV** con las siguientes columnas (mínimas):
   - `date` - Fecha del registro
   - `nps_score` - Score NPS (0-10)
   - `satisfaction_score` - Score de satisfacción (1-5)
   - `converted` - Boolean (True/False) si hubo conversión
   - `visitors` - Número de visitantes
   - `sales` - Monto de ventas
   - `status` - Estado del producto/registro

2. **Coloca el archivo** en: `data/tu_archivo.csv`

3. **Modifica** `data_analyzer.py` línea 295:
   ```python
   analyzer.load_data('data/tu_archivo.csv')  # Cambia aquí
   ```

4. **Ejecuta** normalmente:
   ```bash
   python data_analyzer.py
   ```

## Ejecutar Todo en un Solo Paso

Si quieres ejecutar todo de una vez:

```bash
# Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# Ejecutar análisis completo
python data_analyzer.py

# Generar archivos para dashboards
python dashboard_generator.py
```

## Integrar con Herramientas de BI

### Tableau
1. Abre Tableau Desktop
2. Conecta a archivo de texto
3. Selecciona `tableau_data.csv`
4. Arrastra las métricas a tu dashboard

### Power BI
1. Abre Power BI Desktop
2. Obtener datos > Archivo > JSON
3. Selecciona `powerbi_data.json`
4. Crea visualizaciones con los KPIs

### Looker Studio / Big Query
1. Importa `kpis_summary.csv` como fuente de datos
2. Crea gráficos y tablas con las métricas
3. Configura actualizaciones automáticas si es necesario

## Solución de Problemas

### Error: "ModuleNotFoundError"
**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError"
**Solución**: Asegúrate de ejecutar desde el directorio correcto:
```bash
cd C:\Users\josef\github\business-analytics-dashboard
```

### Error: "No such file or directory: 'data/'"
**Solución**: El script crea la carpeta automáticamente. Si persiste:
```bash
mkdir data
```

## Ejemplo de Uso Programático

También puedes usar el código como librería:

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

# Obtener reporte
print(analyzer.get_summary_report())

# Exportar para dashboard
analyzer.export_to_json('mi_dashboard.json')
```

## Notas Adicionales

- Los datos de ejemplo se generan automáticamente si no tienes datos propios
- Los KPIs se calculan en tiempo real desde los datos
- Los archivos generados están listos para importar en herramientas de BI
- El código es modular y fácil de extender con nuevos KPIs

---

**¡Listo!** Ahora tienes un sistema completo de análisis de KPIs funcionando. 🚀
