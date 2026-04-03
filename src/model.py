import pandas as pd
import sqlite3
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

DB_PATH = "db/logs.db"

def run_anomaly_detection(contamination=0.05):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM logs", conn)

    if len(df) == 0:
        print("[Modelo] No hay datos en la base de datos")
        return 0

    # Encodear columnas de texto a números
    le = LabelEncoder()
    df["protocol_enc"] = le.fit_transform(df["protocol"])
    df["src_ip_enc"] = le.fit_transform(df["src_ip"])

    # Features que usa el modelo
    features = ["src_ip_enc", "dst_port", "bytes_kb", "hour", "protocol_enc"]
    X = df[features].fillna(0)

    # Entrenar y predecir
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )
    preds = model.fit_predict(X)

    # -1 significa anómalo, convertimos a 0/1
    df["anomaly"] = (preds == -1).astype(int)

    # Guardar resultados en SQLite
    conn.execute("UPDATE logs SET anomaly = 0")
    conn.commit()
    for _, row in df[df["anomaly"] == 1].iterrows():
        conn.execute(f"UPDATE logs SET anomaly=1 WHERE id={row['id']}")
    conn.commit()
    conn.close()

    total = int(df["anomaly"].sum())
    print(f"[Modelo] Detección completa: {total} anomalías encontradas")
    return total