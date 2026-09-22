import streamlit as st
import requests
from datetime import datetime

# === CONFIGURAÇÃO DA PÁGINA ===
st.set_page_config(
    page_title="GECOM — Emergência",
    page_icon="🚨",
    layout="centered"
)

API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}",
    "Content-Type": "application/json"
}

# === PEGA DADOS DA URL ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# Converte coordenadas para endereço
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

# === CABEÇALHO — UMA VEZ SÓ ===
st.markdown("""
<h1 style='text-align: center; color: #d32f2f;'>🚨 GECOM SEGURANÇA — Emergência</h1>
<h3 style='text-align: center;'>Proteção Máxima · Campo Bom / RS</h3>
<hr style='border: 1px solid #ddd; margin: 20px 0;'>
""", unsafe_allow_html=True)

# === BOTÃO DE CAPTURA ===
if not lat or not lon:
    st.info("📌 Clique no botão abaixo e PERMITA a localização quando solicitado:")
    
    st.components.v1.html("""
<div style="margin: 15px 0;">
<button onclick="capturarGPS()" style="width:100%; padding:18px; font-size:20px; background-color:#ff3333; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="status" style="margin-top:12px; color:#555; text-align:center;"></p>
</div>

<script>
function capturarGPS() {
    const status = document.getElementById("status");
    status.textContent = "🔄 Buscando localização...";
    
    if (!navigator.geolocation) {
        status.textContent = "❌ Navegador não suporta GPS — preencha abaixo";
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            const url = new URL(window.location.href);
            url.searchParams.set("lat", pos.coords.latitude);
            url.searchParams.set("lon", pos.coords.longitude);
            window.location.href = url.toString();
        },
        function(erro) {
            let msg = "⚠️ ";
            if (erro.code === 1) msg += "Permita a localização no 🔒 cadeado acima";
            else msg += "Preencha manualmente os campos abaixo";
            status.textContent = msg;
        },
        {enableHighAccuracy: true, timeout: 15000}
    );
}
</script>
""", height=200)
    
    st.warning("👇 Preencha manualmente se o GPS não funcionar:")
else:
    st.success("✅ Localização capturada com sucesso!")

st.markdown("<hr style='border: 1px solid #eee; margin: 20px 0;'>", unsafe_allow_html=True)

# === FORMULÁRIO — SEMPRE APARECE ===
with st.form("formulario_alerta"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=lon)
    
    endereco = st.text_input("🏠 Endereço Completo", value=endereco_auto)
    obs = st.text_area("📝 O que está acontecendo?")
    
    enviar = st.form_submit_button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True)

# === PROCESSAR ENVIO ===
if enviar:
    if not nome:
        st.error("❌ Por favor, digite seu nome!")
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
                st.markdown(f"🔗 [Abrir localização no Google Maps]({dados['mapa']})")
        else:
            st.error(f"❌ Erro ao enviar: código {resp.status_code}")

st.markdown("""
<div style='text-align: center; margin-top: 30px; color: #666; font-size: 14px;'>
GECOM Segurança — Proteção Máxima · Emergência: 190
</div>
""", unsafe_allow_html=True)
                            
