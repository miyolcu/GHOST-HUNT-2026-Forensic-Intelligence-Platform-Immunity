import sqlite3
import pandas as pd
import multiprocessing
import os
import numpy as np
from collections import Counter

def calculate_entropy_and_rhythm(db_path):
    conn = sqlite3.connect(db_path)
    # Hayalet grubun verilerini zaman sırasına göre çekiyoruz
    query = """
    SELECT created_at, full_text 
    FROM tweets 
    WHERE user_screen_name = '' OR user_screen_name IS NULL
    ORDER BY created_at ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty: return None

    # Zaman analizi (Ritim)
    df['created_at'] = pd.to_datetime(df['created_at'])
    intervals = df['created_at'].diff().dt.total_seconds().dropna()
    
    # Kelime analizi (Entropi - Her 500 tweetlik blokta)
    window_size = 500
    entropy_scores = []
    
    for i in range(0, len(df), window_size):
        block = df['full_text'].iloc[i:i+window_size]
        all_words = " ".join(block).lower().split()
        if not all_words: continue
        unique_words = len(set(all_words))
        ttr = unique_words / len(all_words) # Type-Token Ratio
        entropy_scores.append(ttr)

    return {
        'avg_interval': intervals.mean(),
        'std_interval': intervals.std(), # Bu ne kadar düşükse o kadar 'mekanik' bir bot ritmi var demektir
        'avg_ttr': np.mean(entropy_scores) if entropy_scores else 0
    }

def main():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    print("[*] Bağışıklık Sistemi Teşhis Modülü Çalışıyor...")
    
    with multiprocessing.Pool(processes=len(db_files)) as pool:
        results = [r for r in pool.map(calculate_entropy_and_rhythm, db_files) if r is not None]
    
    # Global İstatistikler
    final_ttr = np.mean([r['avg_ttr'] for r in results])
    final_std = np.mean([r['std_interval'] for r in results])
    
    print("\n" + "="*60)
    print("TEŞHİS RAPORU: OTOİMMÜN PATOLOJİ ANALİZİ")
    print("="*60)
    print(f"1. ANLAMSAL ÇÜRÜME (Avg TTR): {final_ttr:.4f}")
    print(f"   (Organik kitlede > 0.40 beklenir. Düşük değer 'Kısırlık' işaretidir.)")
    print("-"*60)
    print(f"2. RİTMİK ARİTMİ (Interval STD): {final_std:.4f} saniye")
    print(f"   (Düşük varyans, sistemin 'Kalp Atışının' bir yazılım olduğunu kanıtlar.)")
    print("="*60)

if __name__ == "__main__":
    main()