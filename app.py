import streamlit as st
import matplotlib.pyplot as plt
from src.analyzer import (top_source_ips, traffic_by_hour,
                           top_ports, protocol_distribution,
                           anomaly_summary)
from src.model import run_anomaly_detection
from src.database import init_db, insert_logs, query_logs
from src.parser import parse_logs

st.set_page_config(page_title="Log Analyzer", layout="wide")
from src.database import init_db
init_db()
st.title("Analizador de logs de red")
st.caption("Detección de anomalías con Isolation Forest — Portfolio ITS FIME UANL")

# --- Sidebar ---
with st.sidebar:
    st.header("Controles")
    if st.button("Cargar datos de prueba"):
        init_db()
        df = parse_logs("data/raw_logs.csv")
        insert_logs(df)
        st.success(f"{len(df)} registros cargados")

    st.divider()
    contamination = st.slider("Sensibilidad del modelo (%)", 1, 20, 5)
    if st.button("Detectar anomalías"):
        n = run_anomaly_detection(contamination / 100)
        st.success(f"{n} anomalías detectadas")

# --- Métricas ---
summary = anomaly_summary()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total logs", f"{summary['total_logs']:,}")
col2.metric("Anomalías", summary["anomalias"])
col3.metric("% Anómalo", f"{summary['porcentaje']}%")
col4.metric("IPs sospechosas", summary["ips_sospechosas"])

st.divider()

# --- Gráficas ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Tráfico por hora del día")
    df_hour = traffic_by_hour()
    if len(df_hour) > 0:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(df_hour["hour"], df_hour["bytes_kb"], color="#378ADD")
        ax.set_xlabel("Hora")
        ax.set_ylabel("KB transferidos")
        st.pyplot(fig)
    else:
        st.info("Carga los datos primero")

with col_b:
    st.subheader("Top 10 IPs más activas")
    df_ips = top_source_ips()
    if len(df_ips) > 0:
        st.dataframe(df_ips, use_container_width=True)
    else:
        st.info("Carga los datos primero")

st.divider()

# --- Tabla de anomalías ---
st.subheader("Registros anómalos detectados")
df_all = query_logs()
df_anomalies = df_all[df_all["anomaly"] == 1]
if len(df_anomalies) > 0:
    st.dataframe(
        df_anomalies[["timestamp", "src_ip", "dst_port", "bytes_kb", "protocol"]],
        use_container_width=True
    )
else:
    st.info("Corre la detección de anomalías primero")