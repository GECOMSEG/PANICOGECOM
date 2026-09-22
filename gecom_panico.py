import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="GECOM — Pânico",
    page_icon="🚨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}",
    "Content-Type": "application/json"
}

# === PWA ===
st.components.v1.html("""
<meta name="theme-color" content="#ff0000">
<meta name="apple-mobile-web-app-capable" content="yes">
<style>
[data-testid="stToolbar"], .stAppHeader, footer { display: none !important; }
.block-container { padding-top: 1rem !important; }
</style>
""", height=0)

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
            endereco_auto = dados.get("display_name", f"{lat}, {lon}")
    except:
        endereco_auto = f"{lat}, {lon}"

# === TÍTULO ===
st.markdown("""
<h1 style='text-align:center;color:red;font-size:28px;margin:0;'>🚨 GECOM SEGURANÇA</h1>
<p style='text-align:center;margin:5px 0 20px;'>Botão de Pânico</p>
""", unsafe_allow_html=True)

# === ETAPA 1 — LOCALIZAÇÃO ===
if not lat or not lon:
    st.markdown("""
    <h3 style='text-align:center;'>📍 Permita sua localização</h3>
    <p style='text-align:center;color:#666;'>Precisamos saber onde você está para enviar o alerta</p>
    """, unsafe_allow_html=True)
    
    st.components.v1.html("""
    <div style="display:flex;justify-content:center;margin:25px 0;">
        <button onclick="pegarGPS()" style="width:85%;max-width:320px;padding:25px 20px;font-size:22px;background:#ff3333;color:white;border:none;border-radius:16px;font-weight:bold;box-shadow:0 4px 12px rgba(255,0,0,0.3);">
        📍 ENVIAR LOCALIZAÇÃO
        </button>
    </div>
    <script>
    function pegarGPS() {
        if (!navigator.geolocation) { alert("⚠️ Não suportado"); return; }
        navigator.geolocation.getCurrentPosition(
            s => window.location.href = window.location.origin + window.location.pathname + "?lat=" + s.coords.latitude + "&lon=" + s.coords.longitude,
            e => alert("⚠️ Permita localização no 🔒 cadeado"),
            {enableHighAccuracy: true, timeout: 15000}
        );
    }
    </script>
    """, height=180)
    
    st.info("💡 Depois de tocar, aguarde recarregar")
    st.stop()

# === CONFIRMADO ===
st.success("✅ Localização confirmada!")
st.markdown(f"<div style='background:#fff0f0;border-left:4px solid #ff3333;padding:12px;border-radius:6px;'>📍 {endereco_auto}</div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;margin:25px 0 15px;'>Toque para acionar</h3>", unsafe_allow_html=True)

# === BOTÃO — TENTA SEM ACENTO PRIMEIRO ===
if st.button("🚨 PÂNICO", type="primary", use_container_width=True):
    if not lat or not lon:
        st.error("❌ Sem localização")
    else:
        with st.spinner("Enviando..."):
            mapa_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            
            # TENTATIVA 1: sem acento
            dados = {
                "nome": "ALERTA DE PÂNICO",
                "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "lat": lat,
                "lon": lon,
                "endereco": endereco_auto,   # ← SEM ACENTO
                "obs": "Usuário acionou o botão de PÂNICO — ATENÇÃO URGENTE!",
                "mapa": mapa_link
            }
            
            resp = requests.post(API_URL, json=dados, headers=headers)
            
            if resp.status_code in [200, 201]:
                st.balloons()
                st.markdown(f"<div style='background:linear-gradient(135deg,#ff0000,#aa0000);color:white;padding:30px;border-radius:16px;text-align:center;'><h2>✅ ALERTA ENVIADO!</h2><p>Ajuda a caminho</p></div>", unsafe_allow_html=True)
                st.markdown(f"🔗 [Ver no Mapa]({mapa_link})")
            else:
                # TENTATIVA 2: com acento
                dados["endereço"] = dados.pop("endereco")
                resp2 = requests.post(API_URL, json=dados, headers=headers)
                if resp2.status_code in [200, 201]:
                    st.balloons()
                    st.markdown(f"<div style='background:linear-gradient(135deg,#ff0000,#aa0000);color:white;padding:30px;border-radius:16px;text-align:center;'><h2>✅ ALERTA ENVIADO!</h2><p>(com acento)</p></div>", unsafe_allow_html=True)
                    st.markdown(f"🔗 [Ver no Mapa]({mapa_link})")
                else:
                    st.error(f"❌ Erro em ambos os formatos")
                    st.info(f"Resposta: {resp.text[:300]}")

st.divider()
st.markdown("""
### 📲 Instalar
- **Android:** ⋮ → **Instalar app** ✅
- **iPhone:** ⬆️ → **Adicionar à Tela de Início** ✅
""")
st.caption("GECOM Segurança")
