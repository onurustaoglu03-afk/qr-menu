import streamlit as st
import os
import base64

# Sayfa Ayarları
st.set_page_config(page_title="Deli2go Shell Kafe", page_icon="🥤", layout="centered")

# Arka plan resmini güvenli bir şekilde yükleme fonksiyonu
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_from_file(bin_file):
    if os.path.exists(bin_file):
        bin_str = get_base64_of_bin_file(bin_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp > div:first-child {{
            background-color: rgba(0, 0, 0, 0.4); /* Karartmayı biraz azalttım görsel netleşsin diye */
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

# Arka planı uygula
set_bg_from_file('background.png')

# --- TASARIM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&display=swap');
    
    /* Header Kartı - Daha yukarıda ve daha şık */
    .header-card {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: -30px; /* Kutuyu yukarı çektik */
        margin-bottom: 60px; /* Altındaki butona mesafe bıraktık */
        backdrop-filter: blur(8px);
    }
    
    h1 {
        color: #FF4B4B;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 38px;
        margin: 0;
    }

    /* Kırmızı Buton - Sayfanın daha altında durması için */
    .stButton > button {
        background: linear-gradient(90deg, #FF4B4B 0%, #CC0000 100%) !important;
        color: white !important;
        height: 4.5em;
        width: 100%;
        border-radius: 18px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.3);
        margin-top: 150px; /* Görselin ortasının açılması için butonu aşağı ittik */
    }

    p, span, label, .stMarkdown {
        color: white !important;
    }
    
    /* Gereksiz boşlukları temizle */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

ADMIN_PASSWORD = "onur123"
IMAGE_FOLDER = "menu_images"

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- MÜŞTERİ EKRANI ---
if st.query_params.get("view") == "customer":
    if "view_clicked" not in st.session_state:
        st.session_state.view_clicked = False

    # Üstteki logo kutusu
    st.markdown('<div class="header-card"><h1>DELİ2GO</h1><p style="margin:0; opacity:0.8; color:white;">Shell Kafe Deneyimi</p></div>', unsafe_allow_html=True)

    if not st.session_state.view_clicked:
        # Orta kısım boş bırakıldı (Görselin görünmesi için)
        st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
        
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
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
            st.warning("Menü şu an güncelleniyor...")

# --- YÖNETİCİ PANELİ ---
else:
    st.title("⚙️ Yönetim Paneli")
    st.markdown("<style>.stApp {background-image: none !important; background-color: #111 !important;}</style>", unsafe_allow_html=True)
    
    pwd = st.text_input("Şifre", type="password")
    if pwd == ADMIN_PASSWORD:
        uploaded = st.file_uploader("Menü Resimlerini Yükle", accept_multiple_files=True)
        if st.button("Menüyü Yayına Al"):
            if uploaded:
                for f in os.listdir(IMAGE_FOLDER): os.remove(os.path.join(IMAGE_FOLDER, f))
                for file in uploaded:
                    with open(os.path.join(IMAGE_FOLDER, file.name), "wb") as f:
                        f.write(file.getvalue())
                st.success("Menü güncellendi!")
