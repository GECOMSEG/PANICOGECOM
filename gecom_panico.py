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

# Pega da URL
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# Converte GPS → Endereço
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
        endereco_auto = ""

# === CABEÇALHO ===
st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# === BOTÃO DE CAPTURA + PREENCHE NA HORA ===
if not lat or not lon:
    st.info("📌 Clique e PERMITA sua localização:")
    
    st.components.v1.html("""
<div style="margin: 10px 0;">
<button onclick="capturarGPS()" style="width:100%; padding:15px; font-size:18px; background:#ff3333; color:white; border:none; border-radius:10px; cursor:pointer;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="aviso" style="margin-top:10px; color:#555;"></p>
</div>

<script>
function capturarGPS() {
    const aviso = document.getElementById("aviso");
    aviso.innerText = "🔄 Buscando...";
    
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            // Guarda valores e recarrega com eles
            window.location.href = 
                window.location.origin + 
                window.location.pathname + 
                "?lat=" + pos.coords.latitude + 
                "&lon=" + pos.coords.longitude;
        },
        function(erro) {
            aviso.innerText = "⚠️ " + (erro.code === 1 
                ? "Clique no 🔒 cadeado → Permitir Localização" 
                : "Preencha manualmente abaixo");
        },
        {enableHighAccuracy: true, timeout: 10000}
    );
}
</script>
""", height=180)
    
    st.warning("👇 Preencha manualmente se o GPS não aparecer:")
else:
    st.success("✅ Localização capturada! Dados já preenchidos abaixo:")

st.divider()

# === FORMULÁRIO SEMPRE VISÍVEL ===
with st.form("alerta"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=lat, key="lat_input")
    with col2:
        lon = st.text_input("📍 Longitude", value=lon, key="lon_input")
    
    endereco = st.text_input("🏠 Endereço Completo", value=endereco_auto, key="end_input")
    obs = st.text_area("📝 O que está acontecendo?", key="obs_input")
    
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
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
