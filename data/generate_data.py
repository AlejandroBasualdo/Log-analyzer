import pandas as pd
import random
import datetime

def generate_logs(n=5000):
    ips = [f"192.168.1.{i}" for i in range(1, 50)]
    attackers = ["10.0.0.99", "172.16.0.1", "192.168.1.200"]
    ports = [80, 443, 22, 21, 3389, 8080, 53]
    rows = []

    for i in range(n):
        ts = datetime.datetime.now() - datetime.timedelta(minutes=i * 2)
        es_atacante = random.random() > 0.95
        src = random.choice(attackers) if es_atacante else random.choice(ips)

        rows.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": src,
            "dst_ip": random.choice(ips),
            "src_port": random.randint(1024, 65535),
            "dst_port": random.choice(ports),
            "bytes": random.randint(50000, 200000) if es_atacante else random.randint(64, 65000),
            "protocol": random.choice(["TCP", "UDP", "ICMP"]),
            "status": "ATTACK" if es_atacante else "NORMAL"
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_logs()
    df.to_csv("data/raw_logs.csv", index=False)
    print(f"Dataset generado: {len(df)} filas en data/raw_logs.csv")