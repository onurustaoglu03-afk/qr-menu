import streamlit as st
import os

st.set_page_config(page_title="Dijital Menü", layout="centered")

# Tasarım
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; height: 5em;
        width: 100%; border-radius: 20px; font-size: 24px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
query_params = st.query_params

# 1. MÜŞTERİ EKRANI
if query_params.get("view") == "customer":
    st.title("🍴 Hoş Geldiniz")
    if os.path.exists("guncel_menu.pdf"):
        with open("guncel_menu.pdf", "rb") as f:
            st.download_button("📖 MENÜYÜ GÖRÜNTÜLE", f, "menu.pdf", "application/pdf")
    else:
        st.error("Menü güncelleniyor...")
    st.caption("Unal Grup Dijital Menü")

# 2. YÖNETİCİ PANELİ
else:
    st.title("⚙️ Menü Yönetimi")
    password = st.text_input("Şifre:", type="password")
    
    if password == ADMIN_PASSWORD:
        uploaded_file = st.file_uploader("Yeni PDF Yükle", type="pdf")
        if uploaded_file:
            with open("guncel_menu.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("Menü başarıyla güncellendi! Müşteri linkini yenileyin.")