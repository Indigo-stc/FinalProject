# Informe Técnico – Análisis COVID

## 1. Arquitectura del Pipeline

El pipeline está organizado como un conjunto de **assets en Dagster**, con chequeos de calidad de datos tanto de entrada como de salida.  
Se utilizan las siguientes secciones:

- **Lectura de datos**: asset `covid_data` descarga CSV desde Our World in Data.
- **Chequeos de entrada**: `check_columnas_no_nulas` y `check_unicidad`.
- **Procesamiento**: asset `datos_procesados` filtra países y elimina duplicados/nulos.
- **Métricas**: 
  - `metrica_incidencia_7d`: incidencia acumulada 7 días por 100k habitantes.
  - `metrica_factor_crec_7d`: factor de crecimiento semanal de casos.
- **Chequeos de salida**: `check_factor_crec_irreal` y `check_incidencia_valores`.
- **Reporte final**: `roporte` exporta métricas a Excel.

### Diagrama de Pipeline
<img width="1776" height="521" alt="Screenshot From 2025-08-31 15-09-33" src="https://github.com/user-attachments/assets/0519d403-0534-4cc8-9dad-db94a6066b03" />
