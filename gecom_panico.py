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

# === PEGA GPS E GUARDA ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# Tenta converter GPS → Endereço
endereco_auto = ""
if lat and lon:
    try:
        import json
        import urllib.request
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=pt-BR"
        req = urllib.request.Request(url, headers={"User-Agent": "GECOM/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            dados_end = json.loads(resp.read().decode())
            endereco_auto = dados_end.get("display_name", "")
    except:
        endereco_auto = ""

st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# === BOTÃO DE CAPTURA ===
if not lat or not lon:
    st.info("📌 Clique abaixo e PERMITA a localização:")
    
    st.components.v1.html("""
<button onclick="capturarGPS()" style="width:100%; padding:15px; font-size:18px; background:#ff3333; color:white; border:none; border-radius:10px; cursor:pointer;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="msg" style="margin-top:10px; color:#555;"></p>

<script>
function capturarGPS() {
    const msg = document.getElementById("msg");
    msg.innerText = "🔄 Buscando sinal GPS...";
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            window.location.href = 
                window.location.origin + 
                window.location.pathname + 
                "?lat=" + pos.coords.latitude + 
                "&lon=" + pos.coords.longitude;
        },
        function(erro) {
            if (erro.code === 1) msg.innerText = "⚠️ Permita a localização no 🔒 cadeado acima";
            else if (erro.code === 2) msg.innerText = "⚠️ Sinal não encontrado — preencha abaixo";
            else msg.innerText = "⚠️ Preencha manualmente os campos abaixo";
        },
        {enableHighAccuracy: true, timeout: 15000}
    );
}
</script>
""", height=180)
    st.warning("👇 Preencha manualmente se o GPS não aparecer:")

st.divider()

# === FORMULÁRIO ===
with st.form("alerta"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=lon)
    
    endereco = st.text_input("🏠 Endereço Completo", value=endereco_auto)
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
                st.markdown(f"🔗 [Ver localização no Mapa]({dados['mapa']})")
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
    
