import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="GECOM — Emergência", page_icon="🚨", layout="centered")

# === CONFIGURAÇÃO ===
API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"
# =====================

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}",
    "Content-Type": "application/json"
}

# Inicializa valores na sessão
if "lat" not in st.session_state:
    st.session_state.lat = ""
if "lon" not in st.session_state:
    st.session_state.lon = ""

# Pega da URL se veio
lat_url = st.query_params.get("lat", "")
lon_url = st.query_params.get("lon", "")
if lat_url and lon_url:
    st.session_state.lat = lat_url
    st.session_state.lon = lon_url

st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# Se JÁ tem coordenadas → mostra formulário
if st.session_state.lat and st.session_state.lon:
    st.success("✅ Localização capturada!")
else:
    st.info("📍 Clique no botão abaixo:")
    
    st.components.v1.html("""
<button onclick="pegarGPS()" style="width:100%; padding:15px; font-size:18px; background:#ff3333; color:white; border:none; border-radius:10px; cursor:pointer;">
📌 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="status" style="margin-top:10px;"></p>

<script>
function pegarGPS() {
    document.getElementById("status").innerText = "🔄 Buscando...";
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            const url = new URL(window.location.href);
            url.searchParams.set("lat", pos.coords.latitude);
            url.searchParams.set("lon", pos.coords.longitude);
            window.location.href = url.toString();
        },
        function(erro) {
            document.getElementById("status").innerText = 
                "⚠️ Permita a localização ou preencha abaixo.";
        },
        {enableHighAccuracy: true, timeout: 15000}
    );
}
</script>
""", height=160)

# === FORMULÁRIO SEMPRE VISÍVEL ===
st.divider()
with st.form("form_emergencia"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=st.session_state.lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=st.session_state.lon)
    
    endereco = st.text_input("🏠 Endereço Completo")
    obs = st.text_area("📝 O que está acontecendo?")
    
    enviar = st.form_submit_button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True)

# === ENVIO ===
if enviar:
    if not nome:
        st.error("❌ Digite seu nome!")
    else:
        dados = {
            "nome": nome,
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "endereco": endereco or "Não informado",
            "lat": lat,
            "lon": lon,
            "obs": obs,
            "mapa": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()
            if lat and lon:
                st.markdown(f"🔗 [Ver no Mapa]({dados['mapa']})")
            # Limpa para novo uso
            st.session_state.lat = ""
            st.session_state.lon = ""
        else:
            st.error(f"❌ Erro {resp.status_code}: {resp.text}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
