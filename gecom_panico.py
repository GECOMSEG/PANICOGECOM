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

# Pega da URL
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# === BOTÃO DE CAPTURA ===
if not lat or not lon:
    st.info("📌 Clique e PERMITA quando o navegador pedir!")
    
    st.components.v1.html("""
<div style="text-align:center; margin:10px 0;">
<button onclick="capturarGPS()" style="font-size:20px; padding:15px 30px; background-color:#ff3333; color:white; border:none; border-radius:10px; cursor:pointer; width:100%;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="mensagem" style="margin-top:15px; color:#555;"></p>
</div>

<script>
function capturarGPS() {
    const msg = document.getElementById("mensagem");
    msg.textContent = "🔄 Buscando...";
    
    if (!navigator.geolocation) {
        msg.textContent = "❌ Seu navegador não suporta GPS — preencha abaixo";
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        function(sucesso) {
            const url = new URL(window.location.href);
            url.searchParams.set("lat", sucesso.coords.latitude);
            url.searchParams.set("lon", sucesso.coords.longitude);
            window.location.href = url.toString();
        },
        function(erro) {
            let texto = "⚠️ ";
            if (erro.code === 1) texto += "Clique no 🔒 cadeado ao lado → Permitir Localização";
            else if (erro.code === 2) texto += "Sinal de localização não encontrado";
            else if (erro.code === 3) texto += "Tempo esgotado — tente de novo";
            else texto += "Não foi possível capturar";
            msg.textContent = texto;
        },
        {enableHighAccuracy: true, timeout: 10000, maximumAge: 0}
    );
}
</script>
""", height=200)

st.divider()

# === FORMULÁRIO SEMPRE APARECE ===
with st.form("envio"):
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
            "mapa": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
