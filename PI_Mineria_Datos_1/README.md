# Proyecto Integrador — Minería de Datos I

## Información general

Proyecto integrador de la materia Minería de Datos I (Módulo 3: Modelar y Comunicar). Análisis de los factores que influyen en el costo del seguro médico utilizando técnicas de análisis exploratorio de datos (EDA), reducción de dimensionalidad (PCA) y visualización interactiva con Streamlit.

## Objetivo del proyecto

Identificar los principales determinantes del costo del seguro médico a partir de un dataset de 1,363 asegurados. Se busca comprender qué variables (tabaquismo, edad, IMC, sexo, región, número de hijos) tienen mayor impacto en los costos, aplicando EDA y PCA para reducir la dimensionalidad y comunicar los hallazgos mediante una aplicación interactiva.

## Dataset

Fuente: Costos de seguros médicos (Medical Cost Personal Dataset).

El dataset contiene 1,363 registros con 7 variables: edad (`age`), sexo (`sex`), índice de masa corporal (`bmi`), número de hijos (`children`), condición de fumador (`smoker`), región geográfica (`region`) y costo del seguro (`charges`). Se detectaron 152 valores nulos (102 en `age`, 50 en `bmi`) e inconsistencias en variables categóricas (`sex`: 4 variantes, `smoker`: 4 variantes, `region`: 8 variantes). También se identificaron valores atípicos en `bmi` (≤0 y ≥100) y `children` (<0 y >10). El dataset original se preserva sin modificaciones en `data/raw/`.

## Estructura del repositorio

```
PI_Mineria_Datos_1/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  ← Dataset original
│   └── processed/            ← Dataset limpio
├── notebooks/
│   ├── 01_inspeccion_inicial.ipynb
│   ├── 02_calidad_y_limpieza.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_pca.ipynb
│   └── 05_conclusiones.ipynb
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 01_Dataset.py
│       ├── 02_EDA.py
│       ├── 03_PCA.py
│       └── 04_Conclusiones.py
├── reports/
│   └── informe_final.pdf
└── logs/
    └── pipeline_log.csv
```

## Preparación y calidad de datos

El dataset original presentaba 152 valores nulos (7.48% en `age`, 3.67% en `bmi`) y múltiples inconsistencias: 4 variantes de capitalización en `sex` y `smoker` (ej: female/Female), y 8 variantes en `region` por mezcla de siglas (SE, NE) con nombres completos (southeast, northeast). Se detectaron valores atípicos: `bmi` con 14 registros ≤0 (incluyendo -5) y 6 ≥100 (incluyendo 999); `children` con 2 registros negativos y 8 >10 (incluyendo 15 y 99). Las transformaciones aplicadas incluyeron: estandarización de categóricas a minúsculas, mapeo de siglas regionales a nombres completos, conversión de outliers a NaN, e imputación con mediana en `age` (102), `bmi` (70) y `children` (10). Ver registro completo en [logs/pipeline_log.csv](logs/pipeline_log.csv).

## Resumen del análisis exploratorio

La distribución de costos es asimétrica (skew=1.51, media=$13,256, mediana=$9,361). El tabaquismo es el factor dominante: fumadores pagan en promedio 3.2× más que no fumadores (corr=0.79). La edad muestra correlación positiva moderada (r=0.305) con efecto amplificado en fumadores. El IMC tiene correlación baja. Sexo, región y número de hijos mostraron correlaciones cercanas a cero con el costo. Ver [notebooks/03_eda.ipynb](notebooks/03_eda.ipynb).

## Reducción de dimensionalidad

Se aplicó PCA con StandardScaler sobre 9 variables (age, bmi, children, charges, smoker, sex, y 3 regiones one-hot). Ver [notebooks/04_pca.ipynb](notebooks/04_pca.ipynb). PC1 (dominada por charges, smoker y age) captura el eje de costo/riesgo, confirmando los hallazgos del EDA. PC2 captura variabilidad demográfica y de composición corporal.

## Visualización interactiva

La aplicación Streamlit presenta 5 páginas: Home (contexto y enlaces), Dataset (vista previa y calidad), EDA (5 visualizaciones con interpretación), PCA (varianza explicada y loadings) y Conclusiones (hallazgos, limitaciones y próximos pasos). Disponible en: https://mineria-de-datos.streamlit.app/.

## Cómo ejecutar localmente

```bash
# Clonar repositorio
git clone https://github.com/Jav-mol/Mineria-de-datos.git
cd Mineria-de-datos/PI_Mineria_Datos_1

# Crear entorno virtual e instalar dependencias
python -m venv env
source env/Scripts/activate  # Windows
pip install -r requirements.txt

# Ejecutar notebooks
jupyter notebook notebooks/

# Ejecutar aplicación Streamlit
streamlit run app/Home.py
```

## Conclusiones

El tabaquismo es el factor individual con mayor impacto en el costo del seguro (fumadores pagan >3× más). La edad es un factor secundario relevante, especialmente en interacción con el tabaquismo. El IMC tiene efecto menor. Sexo, región y número de hijos no son determinantes. El PCA confirma que los datos pueden representarse eficientemente en menos dimensiones, con el eje de costo/riesgo definido por tabaquismo y edad. Las principales limitaciones incluyen: calidad de datos originales (152 nulos imputados), alcance limitado de variables (7 variables, sin condiciones médicas ni nivel socioeconómico), y naturaleza observacional del análisis (no causal). Ver [notebooks/05_conclusiones.ipynb](notebooks/05_conclusiones.ipynb), [reports/informe_final.pdf](reports/informe_final.pdf) y [app/](app/).
