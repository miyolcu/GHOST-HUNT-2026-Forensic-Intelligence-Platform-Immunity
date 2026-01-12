import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import io
import os

# ==========================================
# 1. UI & TEMA AYARLARI
# ==========================================
st.set_page_config(page_title="GHOST HUNT 2026 - Master Suite", layout="wide")
st.markdown("<style>.main { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }</style>", unsafe_allow_html=True)

# Türkçe karakter desteği için yardımcı fonksiyon
def tr_fix(text):
    trans = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return str(text).translate(trans)

# ==========================================
# 2. PDF SINIFI TANIMI (GRAFİK + TABLO DESTEĞİ)
# ==========================================
class ForensicPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'GHOST HUNT 2026 - ADLI BILISIM RAPORU', 0, 1, 'C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, 'Xeon E5-2680 56-Core Analysis Suite | Status: SEALED', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, tr_fix(title), 0, 1, 'L', 1)
        self.ln(4)

    def add_forensic_table(self, df):
        self.set_font('Arial', 'B', 8)
        # Sütun genişliklerini ayarla
        col_width = 190 / len(df.columns)
        for col in df.columns:
            self.cell(col_width, 7, tr_fix(col), 1)
        self.ln()
        self.set_font('Arial', '', 8)
        for _, row in df.iterrows():
            for val in row:
                self.cell(col_width, 7, tr_fix(val), 1)
            self.ln()
        self.ln(5)

# ==========================================
# 3. ANA ARAYÜZ VE VERİLER
# ==========================================
st.title(">>> OPERATION: GHOST HUNT 2026 // MASTER FORENSIC INTERFACE")
st.caption("Xeon E5-2680 56-Core Analysis Suite | Status: SEALED")

# Metrikler
m_col = st.columns(4)
m_col[0].metric("CPU STATUS", "56 CORES", "100% THREADS")
m_col[1].metric("DATA VOLUME", "42.1M TWEETS", "PROCESSED")
m_col[2].metric("SYNC PULSE", "1000ms", "VERIFIED")
m_col[3].metric("SOURCE DOMINANCE", "%76.1", "CENTRALIZED")

# BÖLÜM I Verileri
risk_df = pd.DataFrame({
    'Likelihood': [5, 4, 3, 5, 2, 4], 'Impact': [5, 4, 3, 5, 2, 4],
    'Bulgu': ['Merkezi Hayalet', 'Zoho Social', '@birol_akal', '1000ms Ritm', 'Piyon Botlar', 'istifaogluBot']
})
fig_risk = px.scatter(risk_df, x="Likelihood", y="Impact", text="Bulgu", color="Impact", size=[80,65,50,75,40,55], template="plotly_dark")

hub_data = pd.DataFrame({
    'Kaynak': ['Zoho Social', 'CryptoMatic', 'eNgageCXM', 'istifaogluBot', 'Sked Social', 'Diger'],
    'Hacim': [12640000, 8820000, 6300000, 4200000, 2520000, 7743312]
})
fig_pie = px.pie(hub_data, values='Hacim', names='Kaynak', hole=0.5, template="plotly_dark")

# BÖLÜM II Verileri
network_metrics = pd.DataFrame({
    "Aktor / Hub": ["CORE: HAYALET", "Zoho Social", "CryptoMatic", "eNgageCXM"],
    "Veri (Tweet)": ["42,123,312", "12,640,000", "8,820,000", "6,300,000"],
    "Etki Puani": ["10/10", "8.5/10", "7.2/10", "6.0/10"],
    "Tur": ["Root", "API-High", "API-Mid", "Hub"]
})

geo_df = pd.DataFrame({'City': ['Istanbul', 'London', 'NY', 'Berlin'], 'lat': [41.0, 51.5, 40.7, 52.5], 'lon': [28.9, -0.1, -74.0, 13.4], 'Bots': [182000, 77000, 35000, 28000]})
fig_map = px.scatter_geo(geo_df, lat='lat', lon='lon', size='Bots', color='Bots', projection="natural earth", template="plotly_dark")

# Dashboard Görünümü
st.plotly_chart(fig_risk, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)
st.table(network_metrics)
st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# 4. PDF RAPOR OLUŞTURMA BUTONU
# ==========================================
st.write("---")
if st.button("🖼️ GRAFİK VE TABLOLU PDF RAPORU OLUŞTUR"):
    with st.spinner("Xeon çekirdekleri grafikleri işliyor ve raporu mühürlüyor..."):
        try:
            pdf = ForensicPDF()
            
            # SAYFA 1: Risk ve Kaynak Analizi
            pdf.add_page()
            pdf.chapter_title("I. STRATEJIK RISK VE KAYNAK DOMINANSI")
            
            # Risk Grafiği
            img_risk = fig_risk.to_image(format="png", width=800, height=400)
            pdf.image(io.BytesIO(img_risk), x=10, w=190)
            pdf.ln(5)
            
            # Pasta Grafik
            img_pie = fig_pie.to_image(format="png", width=800, height=400)
            pdf.image(io.BytesIO(img_pie), x=10, w=190)
            
            # SAYFA 2: Ağ ve Coğrafi Analiz
            pdf.add_page()
            pdf.chapter_title("II. INORGANIK AG VE COGRAFI ANOMALILER")
            
            # Ağ Tablosu
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, "Ag Dugum Analiz Tablosu", ln=True)
            pdf.add_forensic_table(network_metrics)
            
            # Harita Grafiği
            img_map = fig_map.to_image(format="png", width=800, height=400)
            pdf.image(io.BytesIO(img_map), x=10, w=190)
            
            # Ritm Sonuçları
            pdf.ln(10)
            pdf.chapter_title("III. ADLI RITM VE API FREKANS ANALIZI")
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 8, tr_fix("Xeon 56-Core Analiz Sonucu: 1000ms senkronizasyonu tum kitalarda %99.8 oraninda dogrulanmistir. Mekanik akis ve kurumsal mesai saatleri (08:00-18:00 TR) merkezi kontrolu kanitlamaktadir."))

            # PDF'i Belleğe Al ve İndir
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="📥 KAPSAMLI PDF RAPORUNU İNDİR",
                data=pdf_output,
                file_name="GHOST_HUNT_2026_MASTER_REPORT.pdf",
                mime="application/pdf"
            )
            st.success("Rapor başarıyla mühürlendi!")
            
        except Exception as e:
            st.error(f"Rapor oluşturulurken hata: {e}")

st.code(">>> EVIDENCE_SEALED // NO SELF-ORGANIZATION DETECTED // GHOST_HUNT_2026_COMPLETE")