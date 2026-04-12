import streamlit as st
import os

st.set_page_config(page_title="Dijital Menü", layout="centered")

# Tasarım - Resimlerin arasını ve butonları düzenleyelim
st.markdown("""
    <style>
    .stButton > button {
        background-color: #FF4B4B; color: white; height: 5em;
        width: 100%; border-radius: 20px; font-size: 24px; font-weight: bold;
    }
    img {
        max-width: 100%;
        border-radius: 10px;
        margin-bottom: 15px; /* Resimlerin arasına boşluk */
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
IMAGE_FOLDER = "menu_images" # Resimlerin saklanacağı klasör

# Klasör yoksa oluştur
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

query_params = st.query_params

# 1. MÜŞTERİ EKRANI
if query_params.get("view") == "customer":
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = False

    st.title("🍴 Hoş Geldiniz")
    
    if not st.session_state.view_clicked:
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            st.session_state.view_clicked = True
            st.rerun()
    
    if st.session_state.view_clicked:
        image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.jpg', '.jpeg', '.png'))])
        
        if image_files:
            for img_file in image_files:
                st.image(os.path.join(IMAGE_FOLDER, img_file), use_container_width=True)
            
            if st.button("⬅️ Geri Dön"):
                st.session_state.view_clicked = False
                st.rerun()
        else:
            st.warning("Menü şu an güncelleniyor...")

# 2. YÖNETİCİ PANELİ
else:
    st.title("⚙️ Menü Yönetimi")
    password = st.text_input("Şifre:", type="password")
    if password == ADMIN_PASSWORD:
        st.info("Birden fazla sayfa yükleyebilirsiniz. Sayfaların sırasını dosya isimlerine göre (1.jpg, 2.jpg gibi) düzenleyin.")
        uploaded_files = st.file_uploader("Menü Sayfalarını Seçin", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        if st.button("Menüyü Güncelle"):
            if uploaded_files:
                # Eski resimleri temizle
                for f in os.listdir(IMAGE_FOLDER):
                    os.remove(os.path.join(IMAGE_FOLDER, f))
                
                # Yeni resimleri kaydet
                for uploaded_file in uploaded_files:
                    with open(os.path.join(IMAGE_FOLDER, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getvalue())
                st.success(f"{len(uploaded_files)} sayfa başarıyla yüklendi!")
            else:
                st.error("Lütfen önce dosya seçin.")
