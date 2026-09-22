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

st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# Pega direto da URL
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

if not lat or not lon:
    st.info("📍 Permita a localização quando solicitado 👇")
    st.components.v1.html("""
<button onclick="pegarGPS()" style="padding:10px 20px; font-size:16px; background:#ff4444; color:white; border:none; border-radius:8px; cursor:pointer;">
📌 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="status"></p>

<script>
function pegarGPS() {
    const status = document.getElementById("status");
    status.innerHTML = "Buscando...";
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            status.innerHTML = "✅ Localização pronta!";
            window.location.href = window.location.origin + 
                window.location.pathname + 
                "?lat=" + pos.coords.latitude + 
                "&lon=" + pos.coords.longitude;
        },
        function() {
            status.innerHTML = "❌ Não conseguiu — preencha manualmente";
        },
        {enableHighAccuracy: true, timeout: 10000}
    );
}
</script>
""", height=150)
    st.stop()  # Para até clicar no botão
else:
    st.success("✅ Localização capturada!")

# Formulário com valores preenchidos
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
            "mapa": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.success("✅ ENVIADO PARA A CENTRAL!")
            st.balloons()
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
