import sqlite3
import pandas as pd
import multiprocessing
import os

def analyze_ghost_behavior(db_path):
    conn = sqlite3.connect(db_path)
    
    # Kullanıcı adı boş olan veya en aktif olan o ID'nin detaylarına iniyoruz
    # Burada 'user_screen_name' boş olanları veya senin sonucundaki o ana grubu hedefliyoruz
    query = """
    SELECT created_at, source, full_text
    FROM tweets
    WHERE user_screen_name = '' OR user_screen_name IS NULL
    LIMIT 50000 
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    # İlk veritabanından örnek alarak davranış paternini görelim
    print("[*] 'Hayalet' hesabın davranış kalıpları inceleniyor...")
    sample_df = analyze_ghost_behavior(db_files[0])
    
    # 1. Kaynak Analizi (Hangi uygulama ile atılmış?)
    print("\n[!] KULLANILAN KAYNAKLAR (SOURCES):")
    print(sample_df['source'].value_counts().head())
    
    # 2. Zaman Analizi (Tweetler arası saniye farkı)
    sample_df['created_at'] = pd.to_datetime(sample_df['created_at'])
    sample_df = sample_df.sort_values('created_at')
    sample_df['diff'] = sample_df['created_at'].diff().dt.total_seconds()
    
    print("\n[!] TWEETLER ARASI ORTALAMA SÜRE (SANİYE):")
    print(f"{sample_df['diff'].mean():.2f} saniye")

if __name__ == "__main__":
    main()