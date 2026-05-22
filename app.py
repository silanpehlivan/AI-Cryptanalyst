import streamlit as st
import pandas as pd
import numpy as np
from main_solver import AICryptanalyst
from utils import calculate_ic, calculate_entropy, clean_text

# Set Page Config with collapsed sidebar for more space
st.set_page_config(
    page_title="AI Kripto Çözücü",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Dynamic Web Interface" Feel
st.markdown("""
<style>
    /* Remove top whitespace */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
    }
    header {visibility: hidden;}
    
    /* Background Gradient */
    .stApp {
        background: rgb(2,0,36);
        background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%);
        color: white;
    }

    /* Custom Input Area */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.9);
        border: none;
        border-radius: 15px;
        color: #333;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextArea textarea:focus {
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }

    /* Primary Button Animation */
    .stButton>button {
        width: 100%;
        background-image: linear-gradient(to right, #00c6ff 0%, #0072ff 51%, #00c6ff 100%);
        margin: 10px;
        padding: 15px 45px;
        text-align: center;
        text-transform: uppercase;
        transition: 0.5s;
        background-size: 200% auto;
        color: white;            
        box-shadow: 0 0 20px #eee;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background-position: right center; /* change the direction of the change here */
        color: #fff;
        text-decoration: none;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #00d4ff; 
        text-shadow: 2px 2px 4px #000000;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #dfdfdf;
    }

    /* Result Box with Glassmorphism */
    .result-container {
        background: rgba( 255, 255, 255, 0.1 );
        box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
        backdrop-filter: blur( 4px );
        -webkit-backdrop-filter: blur( 4px );
        border-radius: 10px;
        border: 1px solid rgba( 255, 255, 255, 0.18 );
        padding: 20px;
        margin-top: 20px;
    }
    .result-title {
        color: #00ff88;
        font-size: 24px;
        border-bottom: 2px solid #00ff88;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .result-text {
        font-family: 'Courier New', monospace;
        color: #ffffff;
        font-size: 18px;
        word-wrap: break-word;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #333;
    }
    

    /* Expander Text Fix */
    div[data-testid="stExpanderDetails"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        color: #ffffff;
    }
    
    /* Info Box Styling */
    .stAlert {
        background-color: rgba(0, 100, 200, 0.2) !important;
        border: 1px solid #00d4ff !important;
        color: #ffffff !important;
    }
    .stAlert p {
        color: #ffffff !important;
    }
    
    /* Logo replacement text */
    .logo-text {
        font-size: 40px;
        font-weight: bold;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

</style>
""", unsafe_allow_html=True)

# Initialize Solver
@st.cache_resource
def load_solver():
    return AICryptanalyst()

solver = load_solver()

# Sidebar
with st.sidebar:
    # Replaced broken image with large emoji/text
    st.markdown("<h1 style='text-align: center;'>🔐</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>AI Kripto<br>Analiz</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #dfdfdf; margin-bottom: 20px;'>
        <b>Yapay Zeka Destekli Şifre Kırıcı</b>
        <br>
        <i>Aşağıdaki kartlara tıklayarak algoritmalar hakkında bilgi alabilirsiniz.</i>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🏛️ Caesar (Sezar) Şifrelemesi"):
        st.info("Harfleri alfabede belirli bir sayıda kaydırarak şifreler. Tarihte bilinen en eski şifreleme yöntemlerinden biridir.")
    
    with st.expander("🗝️ Vigenere Şifrelemesi"):
        st.info("Her harf için farklı bir kaydırma miktarı kullanan polialfabetik bir şifrelemedir. Yüzyıllarca kırılamayan şifre olarak bilinirdi.")
        
    with st.expander("📦 Base64 Kodlama"):
        st.info("İkili verileri (binary) metin formatına çevirmek için kullanılır. Bir şifreleme değil, kodlama yöntemidir.")
        
    with st.expander("⚡ XOR Şifrelemesi"):
        st.info("Mantıksal 'veya' işlemi kullanarak veriyi şifreler. Tek kullanımlık anahtar (OTP) ile kullanıldığında kırılamaz.")
        
    st.markdown("---")

# Main Content
col_main, col_padding = st.columns([10, 1])

with col_main:
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 30px;'>Kriptografik Analiz Terminali 🚀</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center;'>
        Şifreli metni girin, AI algoritmayı tespit edip anında çözsün.
    </div>
    """, unsafe_allow_html=True)

    # Input Area
    ciphertext = st.text_area(
        "Şifreli Metin", 
        height=150, 
        placeholder="Şifreli veriyi buraya yapıştırın...",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_btn = st.button("⚡ ANALİZİ BAŞLAT")

    if analyze_btn and ciphertext:
        if len(ciphertext) < 3:
            st.warning("⚠️ Lütfen analiz için geçerli bir metin girin.")
        else:
            with st.spinner('🔄 Sistem Veriyi İşliyor...'):
                try:
                    # 1. Prediction & Solution
                    algo, conf, plaintext, info = solver.solve(ciphertext)
                    
                    # 2. Metrics
                    ic = calculate_ic(ciphertext)
                    entropy = calculate_entropy(ciphertext)
                    
                    st.markdown("---")
                    
                    # Metrics Row
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Algoritma", algo)
                    c2.metric("Güven", f"%{conf*100:.1f}")
                    c3.metric("IC Değeri", f"{ic:.4f}")
                    c4.metric("Entropi", f"{entropy:.4f}")
                    
                    # Result Display
                    st.markdown(f"""
                    <div class="result-container">
                        <div class="result-title">🔓 Çözüm Sonucu</div>
                        <div class="result-text">{plaintext}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Info Expander
                    with st.expander("🛠️ Teknik Detaylar"):
                        st.markdown(f"**Yöntem:** `{info}`")
                        if algo == 'Caesar':
                            st.info("Caesar şifrelemesi, harflerin alfabede belirli bir sayıda kaydırılmasıyla oluşturulur. Frekans analizi ile en olası kaydırma bulundu.")
                        elif algo == 'Vigenere':
                            st.info("Vigenere şifrelemesi, bir anahtar kelime kullanılarak yapılan çoklu Caesar şifrelemesidir. IC analizi ile anahtar uzunluğu bulundu.")
                        elif algo == 'XOR':
                            st.info("XOR işlemi, metnin her baytının bir anahtar ile XORlanmasıdır. Tek baytlık anahtarlar denendi.")
                        elif algo == 'Base64':
                            st.info("Base64 bir şifreleme değil, kodlama yöntemidir. Standart kütüphane kullanılarak çözüldü.")

                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")

    elif analyze_btn and not ciphertext:
        st.error("⚠️ Lütfen işlenecek veriyi girin!")

# Footer
st.markdown("""
<div style='position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(0,0,0,0.5); color: white; text-align: center; padding: 10px; font-size: 12px;'>
    AI Cryptanalyst v1.0 • Powered by TensorFlow & Streamlit
</div>
""", unsafe_allow_html=True)
