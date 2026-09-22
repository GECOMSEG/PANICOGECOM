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

# === PWA — INSTALAÇÃO COMO APP DE VERDADE ===
st.components.v1.html("""
<meta name="theme-color" content="#ff0000">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="GECOM">

<!-- Manifesto → faz aparecer "Instalar" -->
<link rel="manifest" href="data:application/manifest+json;base64,eyJuYW1lIjoiR0VDT00gU8OAbmljbyIsInNob3J0X25hbWUiOiJHRUNPTSIsImRlc2NyaXB0aW9uIjoiQm90w6FvIGRlIFDDoW5pY28gLSBHZWNvbSBTZWd1cmFuY2EiLCJzdGFydF91cmwiOiIvIiwiZGlzcGxheSI6InN0YW5kYWxvbmUiLCJiYWNrZ3JvdW5kX2NvbG9yIjoiIzAwMDAwMCIsInRoZW1lX2NvbG9yIjoiI2ZmMDAwMCIsImljb25zIjpbeyJzcmMiOiJodHRwczovL3ZpYS5wbGFjZWhvbGRlci5jb20vMTkyL0ZGMDAwMC9GRkZGRkY/dGV4dD1HIiwic2l6ZXMiOiIxOTJ8MTkyIiwidHlwZSI6ImltYWdlL3BuZyJdfV0=">

<style>
/* Esconde tudo que não é do app */
[data-testid="stToolbar"], .stAppHeader, footer, .stDeployButton { display: none !important; }
.block-container { padding-top: 0.5rem !important; }
</style>
""", height=0)

# === PEGAR LOCALIZAÇÃO ===
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
        endereco_auto = f"{lat}, {lon}"

# === TELA PRINCIPAL ===
st.markdown("""
<h1 style='text-align:center;color:red;font-size:28px;margin:5px 0;'>🚨 GECOM SEGURANÇA</h1>
<p style='text-align:center;margin:5px 0 15px;'>Botão de Pânico</p>
""", unsafe_allow_html=True)

# === PASSO 1 — CAPTURAR LOCALIZAÇÃO ===
if not lat or not lon:
    st.markdown("""
    <div style='text-align:center;padding:20px 10px;'>
    <h3 style='color:#333;'>📍 Permita sua localização</h3>
    <p style='color:#666;'>Precisamos saber onde você está para enviar o alerta</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.html("""
    <div style="display:flex;justify-content:center;margin:20px 0;">
        <button onclick="pegarLocalizacao()" style="width:85%;max-width:320px;padding:25px 20px;font-size:22px;background:#ff3333;color:white;border:none;border-radius:16px;font-weight:bold;box-shadow:0 4px 12px rgba(255,0,0,0.3);">
        📍 ENVIAR LOCALIZAÇÃO
        </button>
    </div>
    <script>
    function pegarLocalizacao() {
        if (!navigator.geolocation) {
            alert("⚠️ Seu navegador não suporta localização");
            return;
        }
        navigator.geolocation.getCurrentPosition(
            function(sucesso) {
                window.location.href = window.location.origin + window.location.pathname + 
                    "?lat=" + sucesso.coords.latitude + 
                    "&lon=" + sucesso.coords.longitude;
            },
            function(erro) {
                let msg = "⚠️ Não foi possível obter localização\\n";
                if (erro.code === 1) msg += "Toque no 🔒 cadeado → Permitir localização";
                else if (erro.code === 2) msg += "Sinal de GPS fraco — tente ao ar livre";
                else if (erro.code === 3) msg += "Tempo esgotado — tente de novo";
                alert(msg);
            },
            {enableHighAccuracy: true, timeout: 15000, maximumAge: 0}
        );
    }
    </script>
    """, height=180)
    
    st.info("💡 Depois de permitir, a página recarrega sozinha")
    st.stop()

# === PASSO 2 — BOTÃO DE PÂNICO ===
st.success("✅ Localização confirmada!")

st.markdown(f"""
<div style='background:#fff0f0;border-left:4px solid #ff3333;padding:10px 12px;border-radius:6px;margin:15px 0;'>
<strong>📍 Sua posição:</strong><br>
{endereco_auto or f"{lat}, {lon}"}
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;color:#333;margin:20px 0 10px;'>Toque abaixo para acionar</h2>", unsafe_allow_html=True)

# === BOTÃO GIGANTE DE PÂNICO ===
if st.button("🚨 PÂNICO", type="primary", use_container_width=True):
    with st.spinner("Enviando alerta para a central..."):
        mapa_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        
        dados = {
            "nome": "ALERTA DE PÂNICO",
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "endereço": endereco_auto or f"{lat}, {lon}",
            "lat": lat,
            "lon": lon,
            "obs": "Usuário acionou o botão de pânico — ATENÇÃO URGENTE!",
            "mapa": mapa_link
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.balloons()
            st.markdown("""
            <div style='background:linear-gradient(135deg,#ff0000,#cc0000);color:white;padding:30px 20px;border-radius:16px;text-align:center;margin:20px 0;'>
            <h2 style='margin:0;font-size:24px;'>✅ ALERTA ENVIADO!</h2>
            <p style='font-size:16px;margin:10px 0 0;'>A central foi notificada<br>Em breve alguém irá até você</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"🔗 [Ver localização no Mapa]({mapa_link})")
        else:
            st.error(f"❌ Erro ao enviar: {resp.status_code} — tente novamente")

st.divider()

# === INSTRUÇÃO DE INSTALAÇÃO ===
st.markdown("""
### 📲 Instalar na Tela Inicial
- **Android:** toque nos **3 pontinhos ⋮** → **Instalar app** ✅
- **iPhone:** toque em **Compartilhar ⬆️** → **Adicionar à Tela de Início** ✅

Abre direto pelo ícone **GECOM** — sem navegador!
""")

st.caption("GECOM Segurança · Botão de Pânico · Emergência: 190")
