import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="GECOM — Emergência", page_icon="🚨", layout="centered")

API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}",
    "Content-Type": "application/json"
}

lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

endereco_auto = ""
if lat and lon:
    try:
        import json, urllib.request
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=pt-BR"
        req = urllib.request.Request(url, headers={"User-Agent": "GECOM/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            dados = json.loads(resp.read().decode())
            endereco_auto = dados.get("display_name", "")
    except:
        pass

# === ESTILO ===
st.markdown("""
<style>
div[data-testid="stTextInput"] > div > input,
div[data-testid="stTextArea"] > div > textarea {
    font-size: 18px !important;
    padding: 14px 16px !important;
    border-radius: 10px !important;
}
button[kind="primary"] {
    font-size: 18px !important;
    padding: 14px !important;
}
/* Remove espaços e avisos extras */
div[data-testid="stAlert"] { display: none; }
hr { display: none; }
</style>
""", unsafe_allow_html=True)

# === TÍTULO ===
st.markdown("""
<h1 style='text-align: center; color: #d32f2f; margin-bottom: 5px;'>🚨 GECOM SEGURANÇA</h1>
<h4 style='text-align: center; color: #555; margin-top: 0; margin-bottom: 25px;'>Proteção Máxima · Campo Bom / RS</h4>
""", unsafe_allow_html=True)

# === SÓ BOTÃO SE NÃO TIVER GPS ===
if not lat or not lon:
    st.components.v1.html("""
<button onclick="capturarGPS()" style="width:100%; padding:18px; font-size:20px; background:#ff3333; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold; margin-bottom:20px;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>

<script>
function capturarGPS() {
    navigator.geolocation.getCurrentPosition(
        function(sucesso) {
            window.location.href = 
                window.location.origin + 
                window.location.pathname + 
                "?lat=" + sucesso.coords.latitude + 
                "&lon=" + sucesso.coords.longitude;
        },
        function(erro) {},
        {enableHighAccuracy: true, timeout: 15000}
    );
}
</script>


st.caption("GECOM Segurança · Emergência: 190")
