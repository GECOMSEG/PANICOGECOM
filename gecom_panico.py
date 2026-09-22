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

# Converte para endereço
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

# === TÍTULO COMPLETO ===
st.markdown("""
<h1 style='text-align: center; color: #d32f2f;'>🚨 GECOM SEGURANÇA</h1>
<h3 style='text-align: center;'>Proteção Máxima · Campo Bom / RS</h3>
<hr style='border: 1px solid #ddd; margin: 20px 0;'>
""", unsafe_allow_html=True)

# === BOTÃO DE GPS — SEMPRE APARECE ===
st.info("📌 Clique abaixo para capturar sua localização:")

st.components.v1.html("""
<button onclick="capturarGPS()" style="width:100%; padding:18px; font-size:20px; background-color:#ff3333; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">
📍 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<p id="status" style="margin-top:15px; color:#555; text-align:center;"></p>

<script>
function capturarGPS() {
    const status = document.getElementById("status");
    status.textContent = "🔄 Buscando sinal GPS...";
    
    if (!navigator.geolocation) {
        status.textContent = "❌ Navegador não suporta GPS — preencha abaixo";
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
            let mensagem = "⚠️ ";
            if (erro.code === 1) {
                mensagem += "Permita a localização no 🔒 cadeado acima → recarregue a página";
            } else if (erro.code === 2) {
                mensagem += "Sinal não encontrado — preencha manualmente";
            } else {
                mensagem += "Preencha manualmente os campos abaixo";
            }
            status.textContent = mensagem;
        },
        {enableHighAccuracy: true, timeout: 15000}
    );
}
</script>
""", height=220)

st.warning("👇 Preencha manualmente se o GPS não funcionar:")
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
        
