import pandas as pd

# [1] Cargar el CSV
df = pd.read_csv("compact.csv")

# [2] Columnas y tipos de datos
columnas_tipos = df.dtypes

# [3] Mínimo y máximo de new_cases
min_new_cases = df["new_cases"].min()
max_new_cases = df["new_cases"].max()

# [4] Porcentaje de valores faltantes
faltantes_new_cases = df["new_cases"].isna().mean() * 100
faltantes_people_vaccinated = df["people_vaccinated"].isna().mean() * 100

# [5] Rango de fechas
fecha_min = df["date"].min()
fecha_max = df["date"].max()

# [6] Crear DataFrame de perfilado
perfilado = pd.DataFrame({
    "columna": ["new_cases", "people_vaccinated"],
    "tipo_dato": [df["new_cases"].dtype, df["people_vaccinated"].dtype],
    "min": [min_new_cases, None],
    "max": [max_new_cases, None],
    "%_faltantes": [faltantes_new_cases, faltantes_people_vaccinated],
    "fecha_min": [fecha_min, fecha_min],
    "fecha_max": [fecha_max, fecha_max]
})

# 7. Guardar a CSV
perfilado.to_csv("tabla_perfilado.csv", index=False)

print("Perfilado guardado en tabla_perfilado.csv")
