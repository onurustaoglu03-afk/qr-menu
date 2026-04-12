import streamlit as st
import os

st.set_page_config(page_title="Dijital Menü", layout="centered")

# Tasarım - Butonu iyice belirgin ve şık yapalım
st.markdown("""
    <style>
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        height: 6em;
        width: 100%;
        border-radius: 20px;
        font-size: 26px;
        font-weight: bold;
        box-shadow: 0px 10px 20px rgba(255, 75, 75, 0.3);
        border: none;
    }
    .stApp {
        background-color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
query_params = st.query_params

# 1. MÜŞTERİ EKRANI
if query_params.get("view") == "customer":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🍴 Hoş Geldiniz")
    st.write("Menümüzü tam ekran incelemek için aşağıdaki butona dokunun.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if os.path.exists("guncel_menu.pdf"):
        # PDF'i doğrudan Streamlit'in statik dosya sunucusu gibi açıyoruz
        with open("guncel_menu.pdf", "rb") as f:
            st.download_button(
                label="📖 MENÜYÜ TAM EKRAN AÇ",
                data=f,
                file_name="menu.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        st.info("💡 İpucu: Butona bastığınızda menü açılmazsa 'İndir/Aç' seçeneğine onay verin.")
    else:
        st.error("Menü güncelleniyor, lütfen bekleyin...")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Unal Grup | Dijital Menü Sistemi")

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
