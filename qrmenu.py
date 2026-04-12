import streamlit as st
import os

st.set_page_config(page_title="Dijital Menü", layout="centered")

# Tasarım - Buton ve Görsel Ayarları
st.markdown("""
    <style>
    .stButton > button {
        background-color: #FF4B4B; color: white; height: 5em;
        width: 100%; border-radius: 20px; font-size: 24px; font-weight: bold;
    }
    img {
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
query_params = st.query_params

# 1. MÜŞTERİ EKRANI
if query_params.get("view") == "customer":
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = False

    st.title("🍴 Hoş Geldiniz")
    
    if not st.session_state.view_clicked:
        st.write("Menümüzü görüntülemek için butona dokunun.")
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            st.session_state.view_clicked = True
            st.rerun()
    
    if st.session_state.view_clicked:
        # Menü resmini gösteriyoruz (Daha hızlı ve indirme istemez)
        if os.path.exists("menu_resmi.jpg"):
            st.image("menu_resmi.jpg", use_container_width=True)
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
        uploaded_file = st.file_uploader("Menü Görselini Yükle (JPG/PNG)", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            with open("menu_resmi.jpg", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("Menü görseli güncellendi!")
