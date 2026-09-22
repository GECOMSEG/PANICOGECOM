import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="GECOM — Emergência", page_icon="🚨", layout="centered")

# === CONFIGURAÇÃO ===
API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "COLA_A_PUBLISHABLE_KEY_AQUI"
# =====================

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}",
    "Content-Type": "application/json"
}

st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# === INICIALIZA VARIÁVEIS ===
if "lat" not in st.session_state:
    st.session_state.lat = ""
if "lon" not in st.session_state:
    st.session_state.lon = ""
if "endereco" not in st.session_state:
    st.session_state.endereco = ""

# === PEGA LOCALIZAÇÃO — MÉTODO CONFIÁVEL ===
st.info("📍 Solicitando localização...")

# HTML com retorno garantido
gps_html = """
<div id="status">Aguardando permissão...</div>
<script>
navigator.geolocation.getCurrentPosition(
    function(pos) {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        document.getElementById("status").innerHTML = 
            "✅ Localização obtida! Lat: " + lat + ", Lon: " + lon;
        // Envia para o Streamlit via URL
        window.location.href = window.location.origin + 
            window.location.pathname + "?lat=" + lat + "&lon=" + lon;
    },
    function(erro) {
        let msg = "Erro: ";
        if (erro.code === 1) msg += "Permita a localização!";
        else if (erro.code === 2) msg += "Não foi encontrado sinal GPS";
        else msg += "Tempo esgotado";
        document.getElementById("status").innerHTML = "❌ " + msg;
    },
    {enableHighAccuracy: true, timeout: 8000, maximumAge: 0}
);
</script>
"""

# Lê da URL se já veio
params = st.query_params
if "lat" in params and "lon" in params:
    st.session_state.lat = params["lat"]
    st.session_state.lon = params["lon"]
    st.success("✅ Localização carregada!")
else:
    st.components.v1.html(gps_html, height=100)
    st.warning("👆 Permita a localização quando aparecer acima!")
    st.stop()  # Espera recarregar com os dados

# === FORMULÁRIO ===
with st.form("form_chamada"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=st.session_state.lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=st.session_state.lon)
    
    endereco = st.text_input("🏠 Endereço (confirme ou altere)")
    obs = st.text_area("📝 O que está acontecendo?")
    
    enviado = st.form_submit_button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True)

# === ENVIA ===
if enviado:
    if not nome:
        st.error("❌ Digite seu nome!")
    else:
        dados = {
            "nome": nome,
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "endereço": endereco or "Não informado",
            "lat": lat,
            "lon": lon,
            "obs": obs,
            "mapa": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.success("✅ ALERTA ENVIADO! A Central foi notificada!")
            st.balloons()
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
    
