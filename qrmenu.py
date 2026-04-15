import streamlit as st
import os
import time

# Sayfa Ayarları - Burası Streamlit'in kendi Dark Mode ayarını tetikler
st.set_page_config(
    page_title="Deli2go Shell Kafe", 
    page_icon="🥤", 
    layout="centered"
)

# --- CSS: DARK MODE ZORLAMASI VE TASARIM ---
st.markdown("""
    <style>
    /* Dark Mode için arka planı ve metni zorla */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Kart ve Resim Tasarımı */
    .stImage > img {
        border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
        margin-top: 10px;
    }

    /* Kırmızı Gelişmiş Buton */
    .stButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        height: 4em;
        width: 100%;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);
    }
    
    /* Başlık stili */
    .main-title {
        color: #FF4B4B;
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
IMAGE_FOLDER = "menu_images"

# Klasörün varlığından emin ol (Hata önleyici)
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- MÜŞTERİ EKRANI ---
if st.query_params.get("view") == "customer":
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = False

    st.markdown('<p class="main-title">DELİ2GO SHELL KAFE</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888;">Keyifli bir mola için menümüzü inceleyin.</p>', unsafe_allow_html=True)

    if not st.session_state.view_clicked:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            st.session_state.view_clicked = True
            st.rerun()
    
    if st.session_state.view_clicked:
        # Resimleri listele
        image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        image_files.sort() # 1.jpg, 2.jpg sırasını korur
        
        if image_files:
            for img_file in image_files:
                img_path = os.path.join(IMAGE_FOLDER, img_file)
                st.image(img_path, use_container_width=True)
            
            if st.button("⬅️ ANA SAYFAYA DÖN"):
                st.session_state.view_clicked = False
                st.rerun()
        else:
            st.info("Menü şu an güncelleniyor... Lütfen sayfayı yenileyin.")

# --- YÖNETİCİ PANELİ ---
else:
    st.title("⚙️ Yönetim Paneli")
    pwd = st.text_input("Şifre", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Giriş Yapıldı")
        uploaded = st.file_uploader("Menü Resimlerini Yükle (Çoklu)", accept_multiple_files=True)
        
        if st.button("SİSTEME YÜKLE"):
            if uploaded:
                # Önce klasörü boşalt
                for f in os.listdir(IMAGE_FOLDER):
                    os.remove(os.path.join(IMAGE_FOLDER, f))
                
                # Yeni resimleri kaydet
                for file in uploaded:
                    with open(os.path.join(IMAGE_FOLDER, file.name), "wb") as f:
                        f.write(file.getvalue())
                st.success("Menü başarıyla yüklendi! Lütfen müşteri ekranından kontrol edin.")
                st.balloons()

    st.markdown("<br><br><p style='font-size:10px; opacity:0.3;'>Unal Grup</p>", unsafe_allow_html=True)
