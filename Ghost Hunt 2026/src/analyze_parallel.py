import sqlite3
import pandas as pd
import multiprocessing
import os
from collections import Counter

# 1. İşçi Fonksiyonu: Her çekirdek bir DB dosyasını ısırır
def analyze_single_db(db_path):
    db_name = os.path.basename(db_path)
    # Belleği yormamak için her worker kendi bağlantısını açar
    conn = sqlite3.connect(db_path)
    
    print(f"[*] Başlatıldı: {db_name} (PID: {os.getpid()})")
    
    # Koordinasyon Analizi Sorgusu
    # h1 ve h2 join'i ile aynı tweet içindeki hashtag çiftlerini buluruz
    query = """
    SELECT h1.hashtag_text as tag1, h2.hashtag_text as tag2
    FROM hashtags h1
    JOIN hashtags h2 ON h1.tweet_id = h2.tweet_id
    WHERE h1.hashtag_text < h2.hashtag_text
    """
    
    local_counter = Counter()
    
    try:
        # Chunksize ile 42 milyonu parça parça yutuyoruz
        for chunk in pd.read_sql_query(query, conn, chunksize=200000):
            # Çiftleri tuple olarak birleştirip sayıyoruz
            pairs = zip(chunk['tag1'], chunk['tag2'])
            local_counter.update(pairs)
    except Exception as e:
        print(f"[!] Hata ({db_name}): {e}")
    finally:
        conn.close()
        
    print(f"[+] Tamamlandı: {db_name}")
    return local_counter

def main():
    db_folder = r"E:\daily_databases"
    # Tüm veritabanlarını listele
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    # 56 Core gücünü kullan! 
    # db_files sayısı (7) az olduğu için Pool(7) yeterli ama genel yapı için cpu_count bıraktım.
    pool_size = min(len(db_files), multiprocessing.cpu_count())
    
    print(f"--- Global Analiz Başladı ({pool_size} İşçi Çekirdek) ---")
    
    with multiprocessing.Pool(processes=pool_size) as pool:
        # Sonuçları topla (Bu kısım bloklayıcıdır, tüm workerların bitmesini bekler)
        results = pool.map(analyze_single_db, db_files)
    
    # 2. Adım: Tüm çekirdeklerden gelen sonuçları ana bellekte birleştir
    print("\n[*] Tüm sonuçlar birleştiriliyor...")
    final_network = Counter()
    for r in results:
        final_network.update(r)
    
    # 3. Adım: Kriminolojik Bulguyu Yazdır
    print("\n" + "="*50)
    print("EN GÜÇLÜ KOORDİNELİ HASHTAG ÇİFTLERİ")
    print("="*50)
    for (t1, t2), count in final_network.most_common(30):
        print(f"[{count:10,}]  #{t1} <---> #{t2}")

if __name__ == "__main__":
    # Windows için multiprocessing güvenliği
    main()