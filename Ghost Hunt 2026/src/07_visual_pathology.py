import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def create_visual_evidence():
    db_folder = r"E:\daily_databases"
    db_file = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')][0]
    
    conn = sqlite3.connect(db_file)
    query = "SELECT created_at FROM tweets WHERE user_screen_name = '' OR user_screen_name IS NULL LIMIT 10000"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['ts'] = pd.to_datetime(df['created_at'])
    df = df.sort_values('ts')
    df['diff'] = df['ts'].diff().dt.total_seconds()

    # Görselleştirme Ayarları
    plt.figure(figsize=(16, 8))
    sns.set_style("darkgrid")

    # 1. Plot: Zaman-Serisi Ritmi (The Heartbeat)
    plt.subplot(1, 2, 1)
    plt.scatter(range(len(df)), df['diff'], alpha=0.5, s=10, color='#e74c3c')
    plt.ylim(0, 5) # 0-5 saniye arasına odaklanıyoruz
    plt.title("ZAMANSAL ARİTMİ: 'HAYALET' HESAPLARIN KALP ATIŞI", fontsize=14, fontweight='bold')
    plt.xlabel("Tweet Sırası", fontsize=12)
    plt.ylabel("İki Tweet Arası Gecikme (Saniye)", fontsize=12)
    plt.axhline(y=1.0, color='blue', linestyle='--', label='1000ms Mekanik Eşik')
    plt.legend()

    # 2. Plot: Dağılım Yoğunluğu (The Smoking Gun)
    plt.subplot(1, 2, 2)
    sns.histplot(df['diff'].dropna(), bins=100, kde=True, color='#2c3e50')
    plt.xlim(0, 3)
    plt.title("GECİME YOĞUNLUĞU: MEKANİK SENKRONİZASYON", fontsize=14, fontweight='bold')
    plt.xlabel("Gecikme Süresi (Saniye)", fontsize=12)
    plt.ylabel("Frekans", fontsize=12)

    plt.tight_layout()
    plt.savefig('pathology_report.png', dpi=300)
    print("[+] Görsel kanıt 'pathology_report.png' olarak kaydedildi.")
    plt.show()

if __name__ == "__main__":
    create_visual_evidence()