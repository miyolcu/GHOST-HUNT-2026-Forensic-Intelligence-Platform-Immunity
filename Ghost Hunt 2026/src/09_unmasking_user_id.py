import sqlite3
import pandas as pd
import multiprocessing
import os

def find_hidden_user_ids(db_path):
    conn = sqlite3.connect(db_path)
    # user_id sütunu genellikle 'tweets' tablosunda veya 'users' tablosuyla join yapılarak bulunur
    # Pratik bir yaklaşım olarak önce sütun isimlerini kontrol edelim
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(tweets)")
    columns = [col[1] for col in cursor.fetchall()]
    
    query = ""
    if 'user_id' in columns:
        query = "SELECT DISTINCT user_id FROM tweets WHERE user_screen_name = '' OR user_screen_name IS NULL"
    elif 'user_id_str' in columns:
        query = "SELECT DISTINCT user_id_str FROM tweets WHERE user_screen_name = '' OR user_screen_name IS NULL"
    
    if query:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df['user_id'].tolist() if 'user_id' in columns else df['user_id_str'].tolist()
    
    conn.close()
    return []

def main():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    print("[*] Hayalet hesapların UserID bilgileri deşifre ediliyor...")
    
    with multiprocessing.Pool(processes=len(db_files)) as pool:
        results = pool.map(find_hidden_user_ids, db_files)
    
    # Tüm sonuçları tek bir kümede (Set) birleştirerek benzersiz ID'leri bul
    all_user_ids = set()
    for res in results:
        all_user_ids.update(res)
    
    print("\n" + "="*50)
    print(f"TESPİT EDİLEN GİZLİ USER ID'LER ({len(all_user_ids)} Adet)")
    print("="*50)
    for uid in all_user_ids:
        print(f"ID: {uid}")
    print("="*50)

if __name__ == "__main__":
    main()