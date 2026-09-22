import streamlit as st
import requests
from datetime import datetime

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

# === LEITURA DOS DADOS DA URL ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

if lat and lon:
    st.success(f"✅ Localização obtida!")
else:
    st.info("📍 Clique em PERMITIR quando o navegador pedir!")
    st.components.v1.html("""
<script>
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            const url = new URL(window.location.href);
            url.searchParams.set('lat', pos.coords.latitude);
            url.searchParams.set('lon', pos.coords.longitude);
            window.location.href = url.toString();
        },
        function(erro) {
            console.log("GPS indisponível");
        },
        {enableHighAccuracy: true, timeout: 10000}
    );
}
</script>
""", height=0)

# === FORMULÁRIO ===
with st.form("chamada"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=lon)
    
    endereco = st.text_input("🏠 Endereço Completo")
    obs = st.text_area("📝 O que está acontecendo?")
    
    enviar = st.form_submit_button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True)

# === ENVIO — SEM ACENTO NOS CAMPOS ===
if enviar:
    if not nome:
        st.error("❌ Digite seu nome!")
    else:
        dados = {
            "nome": nome,
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "endereco": endereco or "Não informado",  # ✅ SEM ACENTO!
            "lat": lat,
            "lon": lon,
            "obs": obs,
            "mapa": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()
        else:
            st.error(f"❌ Erro {resp.status_code}: {resp.text}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
