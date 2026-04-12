import streamlit as st
import os

# Sayfa başlığı
st.set_page_config(page_title="Deli2go Shell Kafe", layout="centered")

# Tasarım - Buton ve Başlık Renkleri
st.markdown("""
    <style>
    .stButton > button {
        background-color: #FF4B4B; color: white; height: 5em;
        width: 100%; border-radius: 20px; font-size: 24px; font-weight: bold;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
        font-family: 'sans-serif';
    }
    img {
        max-width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
IMAGE_FOLDER = "menu_images"

# Klasör kontrolü
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# URL parametrelerini al
query_params = st.query_params

# --- 1. MÜŞTERİ EKRANI ---
if query_params.get("view") == "customer":
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = False

    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🥤 Deli2go Shell kafeye Hoş Geldiniz")
    
    if not st.session_state.view_clicked:
        st.write("Güncel menümüzü incelemek için butona dokunabilirsiniz.")
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            st.session_state.view_clicked = True
            st.rerun()
    
    if st.session_state.view_clicked:
        image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if image_files:
            for img_file in image_files:
                st.image(os.path.join(IMAGE_FOLDER, img_file), use_container_width=True)
            
            if st.button("⬅️ Geri Dön"):
                st.session_state.view_clicked = False
                st.rerun()
        else:
            st.warning("Menü şu an güncelleniyor, lütfen biraz sonra tekrar deneyin.")
    
    st.caption("Unal Grup Dijital Menü Sistemi")

# --- 2. YÖNETİCİ PANELİ ---
else:
    st.title("⚙️ Yönetim Paneli")
    password = st.text_input("Giriş Şifresi:", type="password")
    
    if password == ADMIN_PASSWORD:
        st.info("Resimleri 1.jpg, 2.jpg gibi isimlendirirseniz sırayla görünürler.")
        uploaded_files = st.file_uploader("Menü Resimlerini Seçin", accept_multiple_files=True)
        
        if st.button("Menüyü Sisteme Yükle"):
            if uploaded_files:
                # Önce eski resimleri temizle
                for f in os.listdir(IMAGE_FOLDER):
                    os.remove(os.path.join(IMAGE_FOLDER, f))
                
                # Yeni dosyaları kaydet
                for uploaded_file in uploaded_files:
                    with open(os.path.join(IMAGE_FOLDER, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getvalue())
                st.success(f"{len(uploaded_files)} sayfa başarıyla yüklendi!")
                st.balloons()
            else:
                st.error("Lütfen önce resim dosyalarını seçin.")
