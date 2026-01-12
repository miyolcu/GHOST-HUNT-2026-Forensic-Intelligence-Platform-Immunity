import sqlite3
import pandas as pd
import multiprocessing
import os
import numpy as np

def analyze_cross_correlation(db_path):
    conn = sqlite3.connect(db_path)
    # Tweetleri milisaniye hassasiyetinde çekiyoruz
    query = """
    SELECT created_at, user_screen_name, id_str
    FROM tweets 
    WHERE user_screen_name = '' OR user_screen_name IS NULL
    ORDER BY created_at ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty: return None

    # Zamanı numerik bir skalaya (unix timestamp) çeviriyoruz
    df['ts'] = pd.to_datetime(df['created_at']).astype(np.int64) // 10**6 # Milliseconds
    
    # "Inter-Event Times": Her olay bir öncekinden ne kadar sonra gerçekleşti?
    df['diff'] = df['ts'].diff().fillna(0)
    
    # Paten analizi: Belirli bir gecikme (lag) yapısı var mı?
    # Eğer sistem bir 'kuyruk' (queue) mantığıyla çalışıyorsa, farklar sabitlenir.
    unique_diffs = df['diff'].value_counts().head(10)
    
    return {
        'total_events': len(df),
        'top_intervals': unique_diffs.to_dict()
    }

def main():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    print("[*] Merkezi Sinir Sistemi Senkronizasyon Analizi Başladı...")
    
    with multiprocessing.Pool(processes=len(db_files)) as pool:
        results = [r for r in pool.map(analyze_cross_correlation, db_files) if r is not None]
    
    # Sonuçları Birleştirme
    combined_intervals = {}
    for r in results:
        for interval, count in r['top_intervals'].items():
            combined_intervals[interval] = combined_intervals.get(interval, 0) + count
            
    print("\n" + "="*60)
    print("SENKRONİZASYON VE KOORDİNASYON İMZASI")
    print("="*60)
    print("En Sık Tekrarlanan Gecikme Süreleri (Milisaniye):")
    # En sık tekrarlanan ilk 5 gecikmeyi görelim
    sorted_intervals = sorted(combined_intervals.items(), key=lambda x: x[1], reverse=True)
    for interval, count in sorted_intervals[:10]:
        if interval > 0:
            print(f"Gecikme: {interval:6.0f} ms | Frekans: {count:8,}")
    print("="*60)

if __name__ == "__main__":
    main()