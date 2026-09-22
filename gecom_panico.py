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

st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# === PEGA VALORES DA URL ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# Se NÃO tem coordenadas → mostra botão para capturar
if not lat or not lon:
    st.info("📍 Clique no botão abaixo para capturar sua localização:")
    
    st.components.v1.html("""
<button onclick="pegarGPS()" style="width:100%; padding:15px; font-size:18px; background:#ff3333; color:white; border:none; border-radius:10px; cursor:pointer;">
📌 CAPTURAR MINHA LOCALIZAÇÃO
</button>
<br>
<p id="aviso" style="color:gray;"></p>

<script>
function pegarGPS() {
    document.getElementById("aviso").innerText = "🔄 Buscando sinal GPS...";
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            const url = new URL(window.location.href);
            url.searchParams.set("lat", pos.coords.latitude);
            url.searchParams.set("lon", pos.coords.longitude);
            window.location.href = url.toString();
        },
        function(erro) {
            document.getElementById("aviso").innerText = 
                "⚠️ Permita a localização ou preencha manualmente abaixo.";
        },
        {enableHighAccuracy: true, timeout: 10000}
    );
}
</script>
""", height=180)
    
    st.stop()  # Espera o usuário capturar

# ✅ TEM COORDENADAS — MOSTRA FORMULÁRIO COMPLETO
st.success("✅ Localização capturada com sucesso!")
st.divider()

with st.form("form_emergencia"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=lat)
    with col2:
        lon = st.text_input("📍 Longitude", value=lon)
    
    endereco = st.text_input("🏠 Endereço Completo")
    obs = st.text_area("📝 O que está acontecendo?")
    
    enviar = st.form_submit_button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True)

# === ENVIA PARA A CENTRAL ===
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
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()
            # Link do mapa
            st.markdown(f"🔗 [Ver no Google Maps]({dados['mapa']})")
        else:
            st.error(f"❌ Erro {resp.status_code}: {resp.text}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
