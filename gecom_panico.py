import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

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

# ✅ Fuso Horário de Brasília (-3h) — SEM precisar instalar nada!
fuso_brasil = timezone(timedelta(hours=-3))

st.components.v1.html("""
<meta name="theme-color" content="#ff0000">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>
[data-testid="stToolbar"], .stAppHeader, footer, .stDeployButton { display: none !important; }
.block-container { padding: 2rem 1rem !important; max-width: 100% !important; }
h1 { font-size: 34px !important; }
</style>
""", height=0)

lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")
nome = st.query_params.get("nome", "CLIENTE GECOM")

endereco = ""
if lat and lon:
    try:
        import json, urllib.request
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=pt-BR"
        req = urllib.request.Request(url, headers={"User-Agent": "GECOM/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            endereco = json.loads(resp.read().decode()).get("display_name", f"{lat}, {lon}")
    except:
        endereco = f"{lat}, {lon}"

if not lat or not lon:
    st.markdown("""
    <h1 style='text-align:center;color:red;margin-bottom:5px;'>🚨 GECOM SEGURANÇA</h1>
    <h2 style='text-align:center;font-size:22px;color:#444;margin:0 0 40px;'>BOTÃO DE PÂNICO</h2>
    <p style='text-align:center;font-size:20px;color:#333;margin-bottom:40px;'>
    Toque abaixo <strong>uma vez</strong> — enviamos sua localização e alerta à central
    </p>
    """, unsafe_allow_html=True)

    st.components.v1.html("""
    <div style="display:flex;justify-content:center;margin:20px 0 40px;">
        <button onclick="acionarPanico()" style="
            width:92%;max-width:360px;
            padding:35px 20px;
            font-size:26px;
            font-weight:bold;
            color:white;
            background:linear-gradient(135deg,#ff1a1a,#b30000);
            border:none;
            border-radius:20px;
            box-shadow:0 8px 25px rgba(255,0,0,0.4);
            cursor:pointer;
        ">
        🚨 PÂNICO — EMERGÊNCIA
        </button>
    </div>
    <script>
    function acionarPanico() {
        if (!navigator.geolocation) {
            alert("⚠️ Seu aparelho não suporta localização");
            return;
        }
        navigator.geolocation.getCurrentPosition(
            function(sucesso) {
                window.location.href = window.location.origin + window.location.pathname + 
                    "?nome=CLIENTE-GECOM" +
                    "&lat=" + sucesso.coords.latitude + 
                    "&lon=" + sucesso.coords.longitude;
            },
            function(erro) {
                let msg = "⚠️ Permita a localização:\\n\\n";
                msg += "→ Toque no 🔒 CADEADO acima → Permitir\\n";
                msg += "→ Depois toque no botão de novo";
                alert(msg);
            },
            {enableHighAccuracy: true, timeout: 20000}
        );
    }
    </script>
    """, height=250)

    st.info("💡 Toque uma vez → permita → a página recarrega sozinha")
    st.stop()

st.success("✅ Localização recebida! Enviando alerta...")
mapa_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

# ✅ HORA CERTA — Horário de Brasília
hora_certa = datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")

dados = {
    "nome": nome,
    "hora": hora_certa,
    "lat": lat,
    "lon": lon,
    "endereco": endereco,
    "obs": "EMERGÊNCIA — Usuário acionou o botão de PÂNICO!",
    "mapa": mapa_link
}

resp = requests.post(API_URL, json=dados, headers=headers)

if resp.status_code in [200, 201]:
    st.balloons()
    st.markdown(f"""
    <div style='
        background:linear-gradient(135deg,#ff0000,#880000);
        color:white;
        padding:40px 20px;
        border-radius:20px;
        text-align:center;
        margin:20px 0;
    '>
        <h2 style='font-size:30px;margin:0;'>✅ ALERTA ENVIADO!</h2>
        <p style='font-size:20px;margin:20px 0 0;'>A central foi notificada às {hora_certa}<br>Ajuda a caminho</p>
    </div>
    <div style='background:#f5f5f5;padding:20px;border-radius:12px;margin-top:20px;'>
        <strong>👤 Nome:</strong> {nome}<br><br>
        <strong>🕐 Hora:</strong> {hora_certa}<br><br>
        <strong>📍 Localização:</strong><br>{endereco}<br><br>
        <a href="{mapa_link}" target="_blank" style="font-size:18px;color:#ff0000;font-weight:bold;">🔗 Ver no Mapa</a>
    </div>
    """, unsafe_allow_html=True)
else:
    dados["endereço"] = dados.pop("endereco")
    resp2 = requests.post(API_URL, json=dados, headers=headers)
    if resp2.status_code in [200, 201]:
        st.balloons()
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#ff0000,#880000);color:white;padding:40px 20px;border-radius:20px;text-align:center;'>
            <h2>✅ ALERTA ENVIADO!</h2>
            <p>Central notificada às {hora_certa}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"🔗 [Ver no Mapa]({mapa_link})")
    else:
        st.error(f"❌ Erro: {resp.text[:250]}")

st.divider()
st.caption("GECOM SEGURANÇA · PROTEÇÃO MÁXIMA · EMERGÊNCIA: (51)99846.3372")
    
