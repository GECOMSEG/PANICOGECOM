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

# === PEGA DA URL ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# Converte GPS → Endereço automático
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

# === CABEÇALHO ÚNICO ===
st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# === BOTÃO DE CAPTURA — SÓ APARECE SE NÃO TIVER LOCALIZAÇÃO ===
if not lat or not lon:
    st.info("📌 Clique abaixo e PERMITA a localização:")
    
    st.components.v1.html("""
<button onclick="capturarGPS()" style="width:100%; padding:15px; font-size:18px; background:#ff3333; color:white; border:none; border-radius:10px; cursor:pointer;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="aviso" style="margin-top:10px; color:#666;"></p>

<script>
function capturarGPS() {
    const aviso = document.getElementById("aviso");
    aviso.innerText = "🔄 Buscando...";
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            window.location.href = 
                window.location.origin + 
                window.location.pathname + 
                "?lat=" + pos.coords.latitude + 
                "&lon=" + pos.coords.longitude;
        },
        function(erro) {
            aviso.innerText = "⚠️ Preencha manualmente os campos abaixo";
        },
        {enableHighAccuracy: true, timeout: 15000}
    );
}
</script>
""", height=170)
    
    st.warning("👇 Preencha manualmente se o GPS não funcionar:")
    st.divider()
else:
    st.success("✅ Localização capturada!")
    st.divider()

# === FORMULÁRIO — APARECE UMA VEZ SÓ ===
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
                st.markdown(f"🔗 [Ver no Mapa]({dados['mapa']})")
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
        
