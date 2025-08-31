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

---

## 2. Justificación de decisiones de diseño

Se uso el diseño ya que permite:

- Uso de **Dagster** para manejar dependencias y assets explícitos.
- Separación clara entre **datos crudos**, **procesados** y **métricas**.
- Uso de `AssetCheckResult` y `blocking=False`para validar reglas sin interrumpir el pipeline completo y obtener las alertas de acorde a los checs.
- Filtrado temprano de datos irrelevantes para mejorar eficiencia y limpieza.

---

## 3. Decisiones de validación

### Entrada
- **Columnas clave no nulas**: `country`, `date`, `population`.  
  Motivación: Estos campos son esenciales para identificar filas únicas y calcular métricas por lo que se debian procesar adecuadamente.
- **Unicidad country+date**: evita duplicados en análisis temporal ya que puedem haber "datos duplicados".

### Salida
- **Factor de crecimiento ≤ 10**: valores mayores son considerados irreales, se considero -->
  En epidemiología y en datos reales de COVID, eso es extremadamente raro salvo por:
  1. Errores en la carga de datos (ej. se reportan varios días juntos).
  2. Correcciones retroactivas (suben datos atrasados todos de golpe).
  3. Cambio en la metodología de conteo de casos.
- **Incidencia acumulada 7 días entre 0 y 2000**: límites basados en plausibilidad epidemiológica.

---

## 4. Descubrimientos importantes

- Presencia de Nulos que podrian afectar si no se realiza un correcto procesamiento.
- Duplicados no detectados.
- Algunos factores de crecimiento extremadamente altos, indicando posibles errores de reporte diario.
- La incidencia semanal es consistente dentro de rangos esperados tras limpieza.

---

## 5. Consideraciones de arquitectura

- Se eligió **pandas** para procesamiento debido a tamaño manejable y familiaridad.
- DuckDB podría mejorar consultas SQL-like, pero no fue necesario para este volumen.
- Soda no se utilizó, se optó por validaciones explícitas con `asset_check` de Dagster.
- Metadata de Dagster permite visualizar resultados de checks directamente en UI.

---

## 6. Resultados

### Métricas

| Métrica | Descripción | Observaciones |
|---------|------------|---------------|
| Incidencia 7d | Casos por 100k habitantes | Promedio móvil suave y razonable |
| Factor de crecimiento | Ratio casos semana actual vs semana anterior | Algunos outliers >10 eliminados para análisis |

### Control de calidad

| Regla | Estado | Filas afectadas |
|-------|--------|----------------|
| Columnas clave no nulas | Falló | 16,958 |
| Unicidad country+date | OK | 0 |
| Factor de crecimiento ≤10 | OK | según país y semana |
| Incidencia 7d 0–2000 | OK | según país y semana |

---



