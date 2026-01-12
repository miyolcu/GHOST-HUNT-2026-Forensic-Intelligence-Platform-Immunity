from fpdf import FPDF
import os

class OperationDossier(FPDF):
    def header(self):
        # Karanlık tema header
        self.set_fill_color(15, 15, 15)
        self.rect(0, 0, 210, 50, 'F')
        self.set_font('Courier', 'B', 24)
        self.set_text_color(0, 255, 0) # Terminal Yeşili
        self.cell(0, 20, '>>> CASE: GHOST_HUNT_2026', 0, 1, 'L')
        self.set_font('Courier', 'B', 10)
        self.cell(0, -5, 'CLASSIFIED // EYES ONLY // ANALYST: ILKER', 0, 1, 'L')
        self.ln(20)

    def chapter_title(self, num, label):
        self.set_font('Courier', 'B', 16)
        self.set_fill_color(40, 40, 40)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, f"SECTION {num}: {label}", 0, 1, 'L', 1)
        self.ln(5)

def build_dossier():
    pdf = OperationDossier()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # SAYFA 1: SİSTEM VE VERİ (SENSÖR ANALİZİ)
    pdf.add_page()
    pdf.chapter_title("01", "HARDWARE & DATA SCAN")
    pdf.set_font('Courier', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, "SYSTEM_LOG: 56 Cores active. 128GB RAM allocated. Scanning 42M data points...\n"
                         "RESULT: Artificial rhythmic patterns detected at 1000ms intervals.")
    if os.path.exists('image_ae7aa4.png'): # Task Manager Görseli
        pdf.image('image_ae7aa4.png', x=10, y=80, w=190)

    # SAYFA 2: HEDEF LİSTESİ (TARGET ACQUISITION)
    pdf.add_page()
    pdf.chapter_title("02", "TARGET ACQUISITION: THE GHOST CORE")
    pdf.set_font('Courier', 'B', 12)
    pdf.cell(0, 10, "PRIMARY NODE: [HIDDEN_USER] | INFLUENCE: 1.000000", 0, 1)
    pdf.set_font('Courier', '', 11)
    pdf.multi_cell(0, 7, "Topological mapping confirms a master-slave relationship across 373,312 nodes.")
    # Buraya 08_infection_network_graph çıktısını tablo olarak veya görsel olarak koyacağız

    # SAYFA 3: ISI HARİTASI (TACTICAL HEATMAP)
    pdf.add_page()
    pdf.chapter_title("03", "LOGISTICS: AUTOMATION FINGERPRINTS")
    if os.path.exists('operation_timezone_final.png'):
        pdf.image('operation_timezone_final.png', x=10, y=50, w=190)
    
    pdf.set_y(170)
    pdf.multi_cell(0, 7, "SIGNAL_ANALYSIS: Evidence of Zoho, CryptoMatic, and RSS injection points.\n"
                         "STATUS: CENTRALIZED COORDINATION CONFIRMED.")

    pdf.output("CYBER_FORENSIC_DOSSIER_ILKER.pdf")
    print("[+] Operasyon Dosyası Mühürlendi: CYBER_FORENSIC_DOSSIER_ILKER.pdf")

build_dossier()