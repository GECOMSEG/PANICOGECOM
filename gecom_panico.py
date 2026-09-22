import streamlit as st
import requests
from datetime import datetime
import json

st.set_page_config(page_title="GECOM — Chamada de Emergência", page_icon="🚨", layout="centered")

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

# === PEGA LOCALIZAÇÃO AUTOMÁTICA ===
st.info("📍 Carregando sua localização...")

# Usando JavaScript para pegar GPS
localizacao = st.components.v1.html("""
<script>
navigator.geolocation.getCurrentPosition(
    (pos) => {
        const dados = {
            lat: pos.coords.latitude,
            lon: pos.coords.longitude,
            precisao: pos.coords.accuracy
        };
        window.parent.postMessage({type: 'gps', dados: dados}, '*');
    },
    (erro) => {
        window.parent.postMessage({type: 'erro', mensagem: 'Permita a localização!'}, '*');
    },
    {enableHighAccuracy: true, timeout: 5000, maximumAge: 0}
);
</script>
""", height=0)

# Campos preenchidos automaticamente
if "lat" not in st.session_state:
    st.session_state.lat = ""
if "lon" not in st.session_state:
    st.session_state.lon = ""
if "endereco_auto" not in st.session_state:
    st.session_state.endereco_auto = ""

# Formulário
with st.form("form_chamada"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=st.session_state.lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=st.session_state.lon)
    
    endereco = st.text_input("🏠 Endereço", value=st.session_state.endereco_auto)
    obs = st.text_area("📝 O que está acontecendo?")
    
    enviado = st.form_submit_button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True)

# Envia para a Central
if enviado:
    if not nome or not endereco:
        st.error("❌ Preencha Nome e Endereço!")
    else:
        dados = {
            "nome": nome,
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "endereço": endereco,
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
            st.error(f"❌ Erro: {resp.status_code} — {resp.text}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
