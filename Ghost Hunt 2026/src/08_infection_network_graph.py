import sqlite3
import pandas as pd
import networkx as nx
import multiprocessing
import os

def build_local_graph(db_path):
    conn = sqlite3.connect(db_path)
    # Hayalet hesapların (kaynak) ve onlarla etkileşime girenlerin (hedef) bağını kuruyoruz
    # Not: RT'ler genelde 'RT @user' şeklinde full_text içinde yer alır
    query = """
    SELECT user_screen_name, full_text 
    FROM tweets 
    WHERE full_text LIKE 'RT @%'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    edges = []
    for _, row in df.iterrows():
        # RT edilen kullanıcıyı metinden ayıkla
        try:
            target = row['full_text'].split('@')[1].split(':')[0].split()[0]
            # Sadece bizim "Hayalet" grubumuza (ismi boş olanlar vb.) yapılan RT'lere odaklanabiliriz
            # Ya da genel yayılımı görmek için tüm RT ağını alabiliriz
            edges.append((row['user_screen_name'], target))
        except:
            continue
    return edges

def main():
    db_folder = r"E:\daily_databases"
    db_files = [os.path.join(db_folder, f) for f in os.listdir(db_folder) if f.endswith('.db')]
    
    print("[*] Enfeksiyon Ağ Haritası Oluşturuluyor (56 Core Parallel)...")
    
    with multiprocessing.Pool(processes=len(db_files)) as pool:
        all_edges = pool.map(build_local_graph, db_files)
    
    # Tüm bağları dev bir grafikte birleştir
    G = nx.Graph()
    for edge_list in all_edges:
        G.add_edges_from(edge_list)
    
    print(f"\n[+] Toplam Düğüm (Kullanıcı) Sayısı: {G.number_of_nodes():,}")
    print(f"[+] Toplam Bağlantı (Etkileşim) Sayısı: {G.number_of_edges():,}")
    
    # En merkezi 'Enfektör' hesapları bul (Degree Centrality)
    centrality = nx.degree_centrality(G)
    top_infectors = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("\n" + "="*50)
    print("ENFEKSİYON MERKEZLERİ (TOP 10 NODES)")
    print("="*50)
    for node, score in top_infectors:
        print(f"Kullanıcı: @{node:20} | Etki Skoru: {score:.6f}")

if __name__ == "__main__":
    main()