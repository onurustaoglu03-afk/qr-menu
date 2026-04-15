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
        /* Görselin üzerine koyu katman (Yazıların okunması için) */
        .stApp > div:first-child {{
            background-color: rgba(0, 0, 0, 0.6);
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
    
    /* Kart Tasarımı */
    .header-card {
        text-align: center;
        padding: 25px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 30px;
        backdrop-filter: blur(5px);
    }
    
    h1 {
        color: #FF4B4B;
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 38px;
        margin: 0;
        letter-spacing: 1px;
    }

    /* Kırmızı Buton */
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
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 12px 20px rgba(255, 75, 75, 0.4);
    }

    /* Yazı Renkleri */
    p, span, label, .stMarkdown {
        color: white !important;
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

    st.markdown('<div class="header-card"><h1>DELİ2GO</h1><p style="margin:0; opacity:0.7;">Shell Kafe Deneyimi</p></div>', unsafe_allow_html=True)

    if not st.session_state.view_clicked:
        st.markdown("<h3 style='text-align:center;'>Hoş Geldiniz!</h3>", unsafe_allow_html=True)
        st.write("<p style='text-align:center; opacity:0.9;'>Kahve keyfinize eşlik edecek menümüzü görmek için dokunun.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📖 MENÜYÜ GÖRÜNTÜLE"):
            st.session_state.view_clicked = True
            st.rerun()
    
    if st.session_state.view_clicked:
        image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if image_files:
            for img_file in image_files:
                st.image(os.path.join(IMAGE_FOLDER, img_file), use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ GERİ DÖN"):
                st.session_state.view_clicked = False
                st.rerun()
        else:
            st.warning("Menü şu an güncelleniyor, lütfen bekleyin...")

# --- YÖNETİCİ PANELİ ---
else:
    st.title("⚙️ Yönetim Paneli")
    # Yönetici panelinde arka planı kapatalım
    st.markdown("<style>.stApp {background-image: none !important; background-color: #111 !important;}</style>", unsafe_allow_html=True)
    
    pwd = st.text_input("Şifre", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Yetki Onaylandı")
        uploaded = st.file_uploader("Menü Sayfalarını Seçin", accept_multiple_files=True)
        if st.button("Menüyü Yayına Al"):
            if uploaded:
                for f in os.listdir(IMAGE_FOLDER): os.remove(os.path.join(IMAGE_FOLDER, f))
                for file in uploaded:
                    with open(os.path.join(IMAGE_FOLDER, file.name), "wb") as f:
                        f.write(file.getvalue())
                st.success("Menü başarıyla güncellendi!")
                st.balloons()
