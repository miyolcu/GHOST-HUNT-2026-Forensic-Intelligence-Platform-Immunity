import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def final_investigation():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    all_data = []
    print("[*] 42 Milyonluk Veri Kümesinde Cerrahi Operasyon Başlatıldı...")
    
    for db in db_files:
        conn = sqlite3.connect(db)
        # NULL değerleri ve boş stringleri elemek için sorguyu güçlendirdik
        query = """
        SELECT created_at, source 
        FROM tweets 
        WHERE (user_screen_name = '' OR user_screen_name IS NULL)
        AND created_at IS NOT NULL
        """
        batch = pd.read_sql_query(query, conn)
        if not batch.empty:
            all_data.append(batch)
        conn.close()
    
    if not all_data:
        print("[!] KRİTİK HATA: Hayalet hesaplara ait zaman verisi bulunamadı!")
        return

    df = pd.concat(all_data)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['hour'] = df['created_at'].dt.hour
    
    # Isı haritası için veriyi hazırlayalım
    pivot_df = df.groupby(['source', 'hour']).size().unstack(fill_value=0)

    if pivot_df.empty:
        print("[!] Veri seti görselleştirme için çok küçük veya boş.")
        return

    # GÖRSELLEŞTİRME
    plt.figure(figsize=(16, 8))
    sns.heatmap(pivot_df, cmap="YlOrRd", annot=True, fmt="d")
    plt.title("HAYALET ORDU MESAİ ÇİZELGESİ: OPERASYON MERKEZİ ANALİZİ", fontsize=14, fontweight='bold')
    plt.xlabel("Günün Saatleri (UTC/Sistem Saati)", fontsize=12)
    plt.ylabel("Saldırı Aracı / Kaynak (Source)", fontsize=12)
    
    plt.tight_layout()
    plt.savefig('operation_timezone_final.png', dpi=300)
    print("\n" + "="*60)
    print("SORUŞTURMA TAMAMLANDI: Isı haritası 'operation_timezone_final.png' olarak kaydedildi.")
    print("="*60)
    plt.show()

if __name__ == "__main__":
    final_investigation()