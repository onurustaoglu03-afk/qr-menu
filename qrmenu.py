import streamlit as st
import os
import base64

st.set_page_config(page_title="Dijital Menü", layout="centered")

# Tasarım Ayarları
st.markdown("""
    <style>
    .menu-button {
        background-color: #FF4B4B;
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 24px;
        font-weight: bold;
        border-radius: 20px;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
query_params = st.query_params

# PDF'i Tarayıcıda Açmak İçin Fonksiyon
def get_pdf_display_link(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # İndirmek yerine tarayıcıda görüntülemeyi tetikleyen link
    return f'<a href="data:application/pdf;base64,{base64_pdf}" class="menu-button" target="_blank">📖 MENÜYÜ GÖRÜNTÜLE</a>'

# 1. MÜŞTERİ EKRANI
if query_params.get("view") == "customer":
    st.title("🍴 Hoş Geldiniz")
    st.write("Menümüzü incelemek için aşağıdaki butona dokunun.")
    
    if os.path.exists("guncel_menu.pdf"):
        # Yeni link butonunu gösteriyoruz
        pdf_link = get_pdf_display_link("guncel_menu.pdf")
        st.markdown(pdf_link, unsafe_allow_html=True)
    else:
        st.error("Menü yükleniyor, lütfen bekleyin...")
    
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
            st.success("Menü güncellendi!")
            st.success("Menü başarıyla güncellendi! Müşteri linkini yenileyin.")
