import sqlite3
import pandas as pd

DB_PATH = "db/logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            bytes_kb REAL,
            protocol TEXT,
            hour INTEGER,
            date TEXT,
            anomaly INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("[DB] Base de datos inicializada")

def insert_logs(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("logs", conn, if_exists="append", index=False)
    conn.close()
    print(f"[DB] {len(df)} registros insertados")

def query_logs() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM logs", conn)
    conn.close()
    return df