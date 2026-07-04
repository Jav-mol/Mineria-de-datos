"""
04_Conclusiones.py — Hallazgos, limitaciones y próximos pasos
"""

import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="🎯", layout="wide")
st.title("🎯 Conclusiones")

st.markdown("---")

# ── Hallazgos ──
st.markdown("## 🔬 Hallazgos principales")

st.markdown("""
A partir del análisis exploratorio y del PCA realizado sobre el dataset de 1,363 asegurados, 
se identificaron los siguientes hallazgos:

| Factor | Impacto en el costo | Evidencia |
|---|---|---|
| **Tabaquismo** | 🔴 **Muy alto** | Fumadores pagan >3× más. Corr = 0.79 |
| **Edad** | 🟠 **Alto** | Corr = 0.30. Efecto amplificado en fumadores |
| **IMC (bmi)** | 🟡 **Bajo** | Correlación positiva pero débil |
| **Sexo** | ⚪ **Nulo** | Sin diferencia significativa |
| **Región** | ⚪ **Nulo** | Sin correlación con el costo |
| **N° de hijos** | ⚪ **Nulo** | Sin correlación con el costo |
""")

st.markdown("""
1. **El tabaquismo es el factor dominante.** Los fumadores pagan en promedio más del triple que los no fumadores, 
   y esta variable explica por sí sola la mayor parte de la variabilidad en los costos.

2. **La edad es un factor secundario pero relevante,** especialmente cuando interactúa con el tabaquismo: 
   los fumadores de mayor edad son el grupo de mayor costo.

3. **El IMC tiene un efecto menor** en comparación con tabaquismo y edad, aunque positivo.

4. **El sexo, la región y el número de hijos no son factores determinantes** del costo del seguro en este dataset.

5. **El PCA confirma que los datos pueden representarse eficientemente en menos dimensiones,** con la primera 
   componente principal capturando el eje de costo/riesgo definido por tabaquismo y edad.
""")

# ── Limitaciones ──
st.markdown("---")
st.markdown("## ⚠️ Limitaciones")

st.markdown("""
Las siguientes limitaciones condicionan el alcance de las conclusiones presentadas:

1. **Calidad de los datos originales:** El dataset contenía 152 valores nulos y múltiples inconsistencias 
   en variables categóricas. Las técnicas de imputación y estandarización aplicadas introducen un grado de 
   incertidumbre en los resultados.

2. **Alcance de las variables disponibles:** El dataset incluye solo 7 variables. Factores potencialmente 
   relevantes como condiciones médicas preexistentes, historial familiar o nivel socioeconómico 
   no están disponibles.

3. **Naturaleza observacional:** El análisis es descriptivo y correlacional. No se pueden establecer 
   relaciones causales entre las variables y el costo del seguro.

4. **Representatividad:** No se dispone de información sobre cómo se recolectaron los datos ni sobre 
   su representatividad respecto a la población general.

5. **Imputación:** La decisión de imputar valores nulos con la mediana puede haber suavizado la 
   variabilidad real de las variables afectadas (age: 102 imputaciones, bmi: 70 imputaciones).
""")

# ── Próximos pasos ──
st.markdown("---")
st.markdown("## 🚀 Próximos pasos")

st.markdown("""
1. **Incorporar variables adicionales:** Incluir información sobre condiciones médicas preexistentes, 
   nivel de actividad física e historial familiar para un modelo más completo.

2. **Aplicar técnicas de imputación más avanzadas:** Utilizar imputación múltiple (MICE) o modelos 
   predictivos (KNN) en lugar de la mediana.

3. **Modelado predictivo:** Extender el análisis hacia modelos supervisados como regresión lineal 
   múltiple, random forest o gradient boosting.

4. **Análisis de interacciones:** Investigar formalmente interacciones entre variables (edad × tabaquismo, 
   bmi × tabaquismo).

5. **Segmentación de asegurados:** Aplicar clustering sobre las componentes principales para identificar 
   perfiles de riesgo diferenciados.

6. **Validación externa:** Contrastar los hallazgos con datasets similares de otras fuentes.
""")
