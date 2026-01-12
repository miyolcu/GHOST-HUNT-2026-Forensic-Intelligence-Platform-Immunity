import sqlite3
import pandas as pd
import multiprocessing
import os  # <--- Eksik olan can kurtaran burası!
from collections import Counter
import re

def clean_text(text):
    if not text: return ""
    # Linkleri, mentionları ve RT ibarelerini temizle
    text = re.sub(r'RT @\w+: ', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    # Noktalama işaretlerini ve sayıları temizle (isteğe bağlı ama DNA analizi için iyidir)
    text = re.sub(r'[^\w\s#]', '', text) 
    return text.lower().strip()

def analyze_content_batch(db_path):
    conn = sqlite3.connect(db_path)
    # Hayalet grubun tweet içeriğini çek
    query = "SELECT full_text FROM tweets WHERE user_screen_name = '' OR user_screen_name IS NULL"
    
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        words = []
        for txt in df['full_text']:
            cleaned = clean_text(txt)
            # 3 harften büyük kelimeleri al
            words.extend([w for w in cleaned.split() if len(w) > 3])
        return Counter(words)
    except Exception as e:
        print(f"[!] Hata {db_path}: {e}")
        return Counter()

def main():
    db_folder = r"E:\daily_databases"
    # os kütüphanesi artık tanımlı:
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    print(f"[*] {len(db_files)} veritabanı üzerinde içerik DNA'sı deşifre ediliyor...")
    
    with multiprocessing.Pool(processes=len(db_files)) as pool:
        results = pool.map(analyze_content_batch, db_files)
    
    global_words = Counter()
    for r in results:
        global_words.update(r)
    
    print("\n" + "="*50)
    print("OPERASYONUN ANAHTAR KELİMELERİ (DNA)")
    print("="*50)
    # En çok kullanılan 40 kelimeyi görelim ki örüntü netleşsin
    for word, count in global_words.most_common(40):
        print(f"{word:25} | {count:10,}")

if __name__ == "__main__":
    main()