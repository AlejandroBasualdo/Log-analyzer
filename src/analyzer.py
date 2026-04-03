import pandas as pd
from src.database import query_logs

def top_source_ips(n=10) -> pd.DataFrame:
    df = query_logs()
    return df.groupby("src_ip")["bytes_kb"].agg(
        total_bytes="sum", conexiones="count"
    ).sort_values("conexiones", ascending=False).head(n).reset_index()

def traffic_by_hour() -> pd.DataFrame:
    df = query_logs()
    return df.groupby("hour")["bytes_kb"].sum().reset_index()

def top_ports() -> pd.DataFrame:
    df = query_logs()
    return df["dst_port"].value_counts().head(10).reset_index()

def protocol_distribution() -> pd.DataFrame:
    df = query_logs()
    return df["protocol"].value_counts().reset_index()

def anomaly_summary() -> dict:
    df = query_logs()
    total = len(df)
    if total == 0:
        return {"total_logs": 0, "anomalias": 0, "porcentaje": 0.0, "ips_sospechosas": 0}
    anomalies = df[df["anomaly"] == 1]
    return {
        "total_logs": total,
        "anomalias": len(anomalies),
        "porcentaje": round(len(anomalies) / total * 100, 2),
        "ips_sospechosas": anomalies["src_ip"].nunique()
    }