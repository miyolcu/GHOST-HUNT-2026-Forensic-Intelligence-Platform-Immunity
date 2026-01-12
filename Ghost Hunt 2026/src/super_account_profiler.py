import sqlite3
import pandas as pd
import multiprocessing
import os
from collections import Counter

def find_super_accounts(db_path):
    conn = sqlite3.connect(db_path)
    # Kritik Hashtag Seti (Analizine göre en çok manipüle edilenleri buraya ekliyoruz)
    target_hashtags = ('AdımFarah', 'BağkurTESCİLMağduriyetineSon', 'Filistin')
    
    query = f"""
    SELECT t.user_screen_name, COUNT(*) as tweet_count
    FROM tweets t
    JOIN hashtags h ON t.id_str = h.tweet_id
    WHERE h.hashtag_text IN {target_hashtags}
    GROUP BY t.user_screen_name
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return Counter(dict(zip(df['user_screen_name'], df['tweet_count'])))

def main():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    with multiprocessing.Pool(processes=len(db_files)) as pool:
        results = pool.map(find_super_accounts, db_files)
    
    global_users = Counter()
    for r in results:
        global_users.update(r)
    
    print("\n" + "="*50)
    print("EN AKTİF 'SÜPER' HESAPLAR (TOP 10)")
    print("="*50)
    for user, count in global_users.most_common(10):
        print(f"User: @{user:20} | Toplam Tweet: {count:,}")

if __name__ == "__main__":
    main()