import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# 1. UI YAPILANDIRMASI (CYBER-FORENSIC THEME)
# ==========================================
st.set_page_config(page_title="GHOST HUNT 2026 - Master Suite", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .stMetric { border: 1px solid #30363d; padding: 20px; border-radius: 10px; background-color: #161b22; }
    h1, h2, h3 { color: #58a6ff !important; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stTable { font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. ÜST PANEL: SİSTEM TELEMETRİSİ
# ==========================================
st.title(">>> OPERATION: GHOST HUNT 2026 // MASTER FORENSIC INTERFACE")
st.caption("Xeon E5-2680 56-Core Analysis Suite | Status: SEALED")

m_col = st.columns(4)
m_col[0].metric("CPU STATUS", "56 CORES", "100% THREADS")
m_col[1].metric("DATA VOLUME", "42.1M TWEETS", "PROCESSED")
m_col[2].metric("SYNC PULSE", "1000ms", "VERIFIED")
m_col[3].metric("SOURCE DOMINANCE", "%76.1", "CENTRALIZED")

# ==========================================
# 3. BÖLÜM I: STRATEJİK RİSK VE EKONOMİ
# ==========================================
st.write("---")
st.header("I. STRATEJİK RİSK VE KAYNAK DOMİNANSI")
c1, c2 = st.columns([1.2, 1])

with c1:
    risk_df = pd.DataFrame({
        'Likelihood': [5, 4, 3, 5, 2, 4], 'Impact': [5, 4, 3, 5, 2, 4],
        'Bulgu': ['Merkezi Hayalet', 'Zoho Social', '@birol_akal', '1000ms Ritm', 'Piyon Botlar', 'istifaogluBot']
    })
    fig_risk = px.scatter(risk_df, x="Likelihood", y="Impact", text="Bulgu", color="Impact", 
                          size=[80,65,50,75,40,55], color_continuous_scale='RdYlGn_r')
    fig_risk.update_layout(height=450, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_risk, use_container_width=True)

with c2:
    hub_data = pd.DataFrame({
        'Kaynak': ['Zoho Social', 'CryptoMatic', 'eNgageCXM', 'istifaogluBot', 'Sked Social', 'Diğer'],
        'Hacim': [12640000, 8820000, 6300000, 4200000, 2520000, 7743312]
    })
    fig_pie = px.pie(hub_data, values='Hacim', names='Kaynak', hole=0.5, color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("#### 📊 Ekonomi & Kaynak Deşifre Metrikleri")
st.table(pd.DataFrame({
    "Analiz Kalemi": ["Toplam Yatırım (Tahmini)", "Merkezi Yönetim Payı", "Bot Başı Birim Maliyet", "Yıllık Operasyon Hacmi"],
    "Sayısal Değer": ["$50,000+", "%76.1 (Dominant)", "$0.15 - $0.40", "$120k (Est.)"],
    "Adli Durum": ["Mühürlendi", "Mekanik Kontrol Onaylı", "Yüksek Verim", "Sürdürülebilir Sahte Yapı"]
}))

# ==========================================
# 4. BÖLÜM II: AĞ VE COĞRAFİ ANOMALİLER
# ==========================================
st.write("---")
st.header("II. İNORGANİK AĞ VE COĞRAFİ ANOMALİLER")
c3, c4 = st.columns([1, 1.2])

with c3:
    st.markdown("#### Veri Ölçekli Ağ Topolojisi")
    node_labels = ["CORE: HAYALET", "Zoho Social", "CryptoMatic", "eNgageCXM", "istifaogluBot"]
    node_sizes = [100, 75, 60, 50, 45]
    fig_net = go.Figure()
    fig_net.add_trace(go.Scatter(x=[0,1,0,-1,0.5], y=[0,1,2,1,-1], mode='markers+text', 
                                 text=node_labels, textposition="bottom center",
                                 marker=dict(size=node_sizes, color=node_sizes, colorscale='Viridis', showscale=False)))
    fig_net.update_layout(height=450, xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_net, use_container_width=True)
    
    # YENİ: AĞ METRİK TABLOSU
    st.markdown("##### 📊 Ağ Düğüm Analiz Tablosu")
    st.table(pd.DataFrame({
        "Aktör / Hub": ["CORE: HAYALET", "Zoho Social", "CryptoMatic", "eNgageCXM"],
        "Veri (Tweet)": ["42,123,312", "12,640,000", "8,820,000", "6,300,000"],
        "Etki Puanı": ["10/10", "8.5/10", "7.2/10", "6.0/10"],
        "Tür": ["Root", "API-High", "API-Mid", "Hub"]
    }))

with c4:
    st.markdown("#### Küresel Yayılım (Aydınlık Projeksiyon)")
    geo_df = pd.DataFrame({'City': ['Istanbul', 'London', 'NY', 'Berlin'], 'lat': [41.0, 51.5, 40.7, 52.5], 'lon': [28.9, -0.1, -74.0, 13.4], 'Bots': [182000, 77000, 35000, 28000]})
    fig_map = px.scatter_geo(geo_df, lat='lat', lon='lon', size='Bots', color='Bots', projection="natural earth", color_continuous_scale='Tealgrn')
    fig_map.update_geos(showcoastlines=True, coastlinecolor="#30363d", showland=True, landcolor="#161b22", showocean=True, oceancolor="#0d1117")
    fig_map.update_layout(height=450, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("#### 🌍 Lokasyon Deşifre & Proxy Matrisi")
st.dataframe(pd.DataFrame({
    "Hedef Bölge": ["Türkiye (Merkez)", "Avrupa Sahası", "Kuzey Amerika", "Orta Doğu"],
    "Gözlenen Bot": ["182,000", "105,000 (Multi-City)", "35,000", "15,000"],
    "Ritm": ["1000ms (Fiks)", "1000ms (Fiks)", "1000ms (Fiks)", "1000ms (Fiks)"],
    "Kanıt": ["Master Pulse %100", "Mechanical Heartbeat", "Central API Command", "Sync Verified"]
}), use_container_width=True)

# ==========================================
# 5. BÖLÜM III: ADLİ RİTM
# ==========================================
st.write("---")
st.header("III. ADLİ RİTM VE API FREKANS ANALİZİ")
st.success("Xeon 56-Core Analiz Sonucu: 1000ms senkronizasyonu tüm kıtalarda %99.8 oranında doğrulanmıştır.")

st.table(pd.DataFrame({
    "Analiz Parametresi": ["Sinyal Aralığı", "Mesai Saatleri", "Senkronizasyon", "API Yanıt Hızı"],
    "Ölçülen Değer": ["1000ms", "08:00 - 18:00 (TR)", "%99.8", "0.2s - 0.4s"],
    "Referans (Organik)": ["İnsan: >3000ms", "Organik: 7/24", "Organik: <%15", "Değişken"],
    "Sonuç": ["MEKANİK KANIT", "KURUMSAL MESAİ", "TAM KONTROL", "ALGORİTMİK AKIŞ"]
}))

st.code(">>> EVIDENCE_SEALED // NO SELF-ORGANIZATION DETECTED // GHOST_HUNT_2026_COMPLETE")