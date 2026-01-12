import sqlite3
import pandas as pd
import os

def get_ghost_tweet_urls():
    db_folder = r"E:\daily_databases"
    # En son tarihli (en güncel) veritabanını seçiyoruz
    db_files = sorted([os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')], reverse=True)
    
    if not db_files: return
    
    conn = sqlite3.connect(db_files[0])
    # Kullanıcı adı boş olan ve belirli anahtar kelimeleri içeren tweetlerin ID'lerini çekiyoruz
    query = """
    SELECT id_str, user_screen_name 
    FROM tweets 
    WHERE (user_screen_name = '' OR user_screen_name IS NULL)
    AND (full_text LIKE '%Kudüs%' OR full_text LIKE '%Staj%' OR full_text LIKE '%Bağkur%')
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print("\n" + "="*70)
    print("HAYALET HESAPLARA AİT DOĞRUDAN TWEET LİNKLERİ")
    print("="*70)
    
    for index, row in df.iterrows():
        # Twitter URL yapısı: twitter.com/anyuser/status/TWEET_ID
        # user_screen_name boş olduğu için 'i' (invisible) veya herhangi bir string kullanılabilir, 
        # çünkü ID doğruysa Twitter sizi doğru hesaba yönlendirir.
        tweet_url = f"https://x.com/i/status/{row['id_str']}"
        print(f"Tweet {index+1}: {tweet_url}")
    
    print("="*70)

if __name__ == "__main__":
    get_ghost_tweet_urls()