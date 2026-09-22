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

lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")

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

# === TÍTULO ===
st.markdown("<h1 style='text-align: center;color: #FF0000'>GECOM SEGURANÇA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #FFFFF0;'>Proteção Máxima · ARARICA/ RS</h4>", unsafe_allow_html=True)
st.divider()

# === BOTÃO — AGORA APARECENDO CERTINHO ===
if not lat or not lon:
    st.markdown("<h3>📍 Capturar Localização</h3>", unsafe_allow_html=True)
    
    # BOTÃO COM ALTURA CERTA — NÃO SOMBRECE MAIS
    st.components.v1.html("""
    <div style="margin: 10px 0 10px 0;">
        <button onclick="capturarGPS()" style="width:100%; padding:18px; font-size:20px; background:#ff3333; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">
        📍 CAPTURAR LOCALIZAÇÃO
        </button>
    </div>
    <script>
    function capturarGPS() {
        navigator.geolocation.getCurrentPosition(
            function(sucesso) {
                window.location.href = window.location.origin + window.location.pathname + "?lat=" + sucesso.coords.latitude + "&lon=" + sucesso.coords.longitude;
            },
            function(erro) { 
                alert("⚠️ Permita a localização: clique no 🔒 cadeado na barra de endereço → Permitir"); 
            },
            {enableHighAccuracy: true, timeout: 15000}
        );
    }
    </script>
    """, height=120)  # ↓ Altura ajustada — botão aparece completo!
    
    st.info("Clique no botão vermelho acima 🔴 → permita localização → página recarrega sozinha ✅")
    st.divider()

# === TABELA — SÓ APARECE DEPOIS DO GPS ===
tem_localizacao = bool(lat and lon)

if tem_localizacao:
    st.markdown("### 📋 Dados da Localização")
    st.success("✅ Capturado pelo GPS")
    st.write("**📍 Latitude:**", lat)
    st.write("**📍 Longitude:**", lon)
    st.write("**🏠 Endereço:**", endereco_auto)
    st.divider()

# === FORMULÁRIO — SEM CAMPOS DUPLICADOS ===
nome = st.text_input("👤 Seu Nome / Razão Social")
obs = st.text_area("📝 O que está acontecendo?", height=150)

enviar = st.button("🚨 ENVIAR ALERTA", type="primary", use_container_width=True, disabled=not tem_localizacao)

# === ENVIO ===
if enviar:
    if not nome:
        st.error("❌ Digite seu nome!")
    else:
        dados = {
            "nome": nome,
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "endereco": endereco_auto or "Não informado",
            "lat": lat,
            "lon": lon,
            "obs": obs,
            "mapa": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()
            st.markdown(f"🔗 [Ver no Mapa]({dados['mapa']})")
        else:
            st.error(f"❌ Erro {resp.status_code}")

st.caption("GECOM Segurança · Emergência: 190")
    
