import streamlit as st
import os
import base64

st.set_page_config(page_title="Dijital Menü", layout="centered")

# Tasarım Ayarları
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #FF4B4B; color: white; height: 5em;
        width: 100%; border-radius: 20px; font-size: 24px; font-weight: bold;
    }
    .pdf-container {
        width: 100%;
        height: 80vh;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
query_params = st.query_params

# 1. MÜŞTERİ EKRANI
if query_params.get("view") == "customer":
    # Session state ile menü açık mı kontrolü
    if "show_menu" not in st.session_state:
        st.session_state.show_menu = False

    st.title("🍴 Hoş Geldiniz")
    
    if not st.session_state.show_menu:
        st.write("Menümüzü incelemek için aşağıdaki butona dokunun.")
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            st.session_state.show_menu = True
            st.rerun()
    
    if st.session_state.show_menu:
        if os.path.exists("guncel_menu.pdf"):
            with open("guncel_menu.pdf", "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # PDF'i bir iframe içinde sayfaya gömüyoruz
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" class="pdf-container" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            if st.button("⬅️ Geri Dön"):
                st.session_state.show_menu = False
                st.rerun()
        else:
            st.error("Menü yükleniyor...")
    
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
