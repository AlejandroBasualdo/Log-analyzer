# Analizador de logs de red

Herramienta de análisis de tráfico de red con detección automática 
de anomalías usando Machine Learning. Desarrollado como proyecto de 
portfolio — ITS FIME UANL.

## ¿Qué hace?

- Procesa archivos de logs de red en formato CSV
- Almacena los registros en una base de datos SQLite
- Detecta comportamientos anómalos usando Isolation Forest
- Muestra un dashboard interactivo con gráficas y alertas en tiempo real

## Tecnologías

- Python 3.14
- Pandas — procesamiento de datos
- scikit-learn — modelo de detección de anomalías (Isolation Forest)
- SQLite — base de datos local
- Streamlit — dashboard web interactivo
- Matplotlib — visualizaciones

## Cómo correrlo localmente
```bash
# 1. Clona el repositorio
git clone https://github.com/AlejandroBasualdo/Log-analyzer.git
cd Log-analyzer

# 2. Crea el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Genera los datos de prueba
python3 data/generate_data.py

# 5. Corre el dashboard
streamlit run app.py
```

## Decisiones técnicas

Se eligió **Isolation Forest** porque es un algoritmo no supervisado: 
no requiere datos etiquetados como "ataque" para entrenarse. Funciona 
aislando puntos que se separan fácilmente del resto, que estadísticamente 
corresponden a comportamientos anómalos. Esto lo hace ideal para tráfico 
de red donde los ataques son una minoría de los registros.

Se usó **SQLite** para eliminar dependencias externas y hacer el proyecto 
completamente portable sin necesidad de un servidor de base de datos.

## Autor

Alejandro Basualdo — ITS FIME UANL
