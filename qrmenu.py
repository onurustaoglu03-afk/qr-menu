import streamlit as st
import os
import time

# Sayfa Ayarları - Tarayıcı sekmesinde görünen isim
st.set_page_config(
    page_title="Deli2go Shell Kafe", 
    page_icon="🥤", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: ARKA PLAN VE GELİŞMİŞ TASARIM ---
st.markdown("""
    <style>
    /* Ana Arkaplan Resmi ve Ayarları */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    .stApp {
        background-image: url('https://raw.githubusercontent.com/onur_unal/qr-menu/main/background.png');
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }

    /* Arka plan üzerine metinlerin okunması için koyu katman */
    .stApp > div {
        background-color: rgba(0, 0, 0, 0.4); /* Kahve görseli üzerine %40 siyah katman */
    }

    /* Kart Tasarımı */
    .stImage > img {
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.7);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease;
    }
    .stImage > img:hover {
        transform: scale(1.02);
    }

    /* Profesyonel Kırmızı Buton */
    .stButton > button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF2B2B 100%);
        color: white;
        height: 4em;
        width: 100%;
        border-radius: 15px;
        font-size: 20px;
        font-weight: 700;
        border: none;
        box-shadow: 0px 8px 20px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 12px 25px rgba(255, 75, 75, 0.6);
        color: white;
    }

    /* Başlık Alanı */
    .header-card {
        text-align: center;
        padding: 30px;
        background: rgba(0, 0, 0, 0.6); /* Başlık arkasına daha koyu katman */
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0px 10px 25px rgba(0,0,0,0.5);
    }
    
    h1 {
        background: -webkit-linear-gradient(#FF4B4B, #FF9B9B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 5px;
        font-size: 36px;
    }
    
    h3, p {
        color: #FFFFFF;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
IMAGE_FOLDER = "menu_images"

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

query_params = st.query_params

# --- 1. MÜŞTERİ EKRANI ---
if query_params.get("view") == "customer":
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = False

    # Üst Alan (Kurumsal Header Kartı)
    st.markdown("""
        <div class="header-card">
            <h1>DELİ2GO</h1>
            <p style="color: #aaa; margin:0; font-size:16px;">Shell Kafe Deneyimi</p>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.view_clicked:
        st.markdown("<h3 style='text-align:center;'>Hoş Geldiniz!</h3>", unsafe_allow_html=True)
        st.write("<p style='text-align:center; color:#ccc;'>Keyifli bir mola için güncel menümüzü inceleyin.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            with st.spinner('Menü hazırlanıyor...'):
                time.sleep(0.5)
                st.session_state.view_clicked = True
                st.rerun()
    
    if st.session_state.view_clicked:
        image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if image_files:
            for img_file in image_files:
                st.image(os.path.join(IMAGE_FOLDER, img_file), use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ ANA SAYFAYA DÖN"):
                st.session_state.view_clicked = False
                st.rerun()
        else:
            st.warning("Menü şu an güncelleniyor, lütfen biraz sonra tekrar deneyin.")

    # Alt Bilgi (Footer)
    st.markdown("<br><hr style='opacity:0.1'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#777; font-size:12px;'>© 2026 Unal Grup | Dijital Menü</p>", unsafe_allow_html=True)

# --- 2. YÖNETİCİ PANELİ (Arka plan buraya uygulanmaz) ---
else:
    # Yönetici panelinin arka planını beyaz yapalım
    st.markdown("""
        <style>
        .stApp {
            background-image: none !important;
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        h1, h3, p { color: #000000 !important; text-align: left;}
        </style>
        """, unsafe_allow_html=True)
        
    st.title("⚙️ Yönetim Paneli")
    password = st.text_input("Giriş Şifresi:", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("Sisteme erişim sağlandı.")
        with st.expander("Menü Sayfalarını Yükle", expanded=True):
            uploaded_files = st.file_uploader("JPG/PNG Formatında Sayfaları Seçin", accept_multiple_files=True)
            
            if st.button("SİSTEMİ GÜNCELLE"):
                if uploaded_files:
                    # Klasörü temizle
                    for f in os.listdir(IMAGE_FOLDER):
                        os.remove(os.path.join(IMAGE_FOLDER, f))
                    
                    # Yeni dosyaları kaydet
                    for uploaded_file in uploaded_files:
                        with open(os.path.join(IMAGE_FOLDER, uploaded_file.name), "wb") as f:
                            f.write(uploaded_file.getvalue())
                    st.success("Dijital menü başarıyla güncellendi!")
                    st.balloons()
                else:
                    st.error("Lütfen önce resim dosyalarını seçin.")
