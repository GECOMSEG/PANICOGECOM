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

# === PEGA VALORES DA URL E GUARDA ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

# Força atualização nos campos
if lat and "lat_salvo" not in st.session_state:
    st.session_state.lat_salvo = lat
    st.session_state.lon_salvo = lon
    st.rerun()  # ✅ Recarrega com os valores carregados

# Usa os valores guardados
lat_final = st.session_state.get("lat_salvo", lat)
lon_final = st.session_state.get("lon_salvo", lon)

# === INTERFACE ===
st.title("🚨 GECOM SEGURANÇA — Emergência")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

if lat_final and lon_final:
    st.success("✅ Localização carregada automaticamente!")
else:
    st.info("📍 Buscando sua localização... permita quando solicitado!")
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
            alert("Não foi possível detectar localização. Preencha manualmente.");
        },
        {enableHighAccuracy: true, timeout: 8000}
    );
} else {
    alert("Navegador não suporta GPS. Preencha manualmente.");
}
</script>
""", height=0)
    st.stop()  # Espera recarregar com os dados

# === FORMULÁRIO ===
with st.form("chamada"):
    nome = st.text_input("👤 Seu Nome / Razão Social")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.text_input("📍 Latitude", value=lat_final)
    with col2:
        lon = st.text_input("📍 Longitude", value=lon_final)
    
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
            # Limpa para novo envio
            st.session_state.pop("lat_salvo", None)
            st.session_state.pop("lon_salvo", None)
        else:
            st.error(f"❌ Erro {resp.status_code}: {resp.text}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
