import sqlite3

def get_db_info(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tablo isimlerini al
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\n--- Veritabanı: {db_path} ---")
    for table in tables:
        table_name = table[0]
        print(f"Tablo: {table_name}")
        
        # Sütun isimlerini ve tiplerini al
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - Sütun: {col[1]} ({col[2]})")
            
        # İlk 1 satırı örnek olarak gör
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
        print(f"  - Örnek Veri: {cursor.fetchone()}")

    conn.close()

# Sadece ilk günü kontrol edelim
get_db_info('E:/daily_databases/tweets_19.db')