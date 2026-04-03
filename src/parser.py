import pandas as pd

def parse_logs(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # Limpiar nulos
    df.dropna(subset=["src_ip", "dst_port", "timestamp"], inplace=True)

    # Convertir timestamp a datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Extraer hora y fecha
    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date.astype(str)

    # Normalizar bytes a KB
    df["bytes_kb"] = (df["bytes"] / 1024).round(2)

    # Filtrar puertos inválidos
    df = df[(df["dst_port"] > 0) & (df["dst_port"] <= 65535)]

    print(f"[Parser] {len(df)} registros cargados y limpios")
    return df