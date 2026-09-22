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

# === PWA — TELA CHEIA, TEXTOS MAIORES ===
st.components.v1.html("""
<meta name="theme-color" content="#ff0000">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>
[data-testid="stToolbar"], .stAppHeader, footer, .stDeployButton { display: none !important; }
.block-container { padding: 1rem 1.5rem !important; max-width: 100% !important; }
div[class*="stAlert"] { font-size: 19px !important; padding: 1.5rem !important; border-radius: 12px !important; }
</style>
""", height=0)

# === PEGAR TUDO JUNTO: NOME + LAT + LON ===
lat = st.query_params.get("lat", "")
lon = st.query_params.get("lon", "")
nome_usuario = st.query_params.get("nome", "")

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

# === TÍTULO GRANDE ===
st.markdown("""
<h1 style='text-align:center;color:red;font-size:36px;margin:10px 0;'>🚨 GECOM SEGURANÇA</h1>
<h2 style='text-align:center;font-size:24px;margin:0 0 30px;'>Botão de Pânico</h2>
""", unsafe_allow_html=True)

# ==================================================
# TELA 1 — UM SÓ BOTÃO → JÁ LEVA TUDO JUNTO
# ==================================================
if not lat or not lon:
    st.markdown("""
    <h3 style='text-align:center;font-size:26px;margin-bottom:15px;'>📍 Permita sua localização</h3>
    <p style='text-align:center;font-size:19px;color:#555;margin-bottom:35px;'>
    Ao tocar, enviamos sua localização e identificação direto à central
    </p>
    """, unsafe_allow_html=True)

    st.components.v1.html("""
    <div style="display:flex;justify-content:center;margin:10px 0 40px;">
        <button onclick="enviarTudo()" style="
            width:92%;max-width:360px;
            padding:30px 20px;
            font-size:24px;
            background:linear-gradient(135deg,#ff2222,#dd0000);
            color:white;
            border:none;
            border-radius:20px;
            font-weight:bold;
            box-shadow:0 6px 20px rgba(255,0,0,0.35);
            cursor:pointer;
        ">
        📍 ENVIAR DADOS E LOCALIZAÇÃO
        </button>
    </div>

    <script>
    function enviarTudo() {
        if (!navigator.geolocation) {
            alert("⚠️ Seu aparelho não suporta localização");
            return;
        }
        navigator.geolocation.getCurrentPosition(
            function(sucesso) {
                // JÁ VAI TUDO JUNTO: nome + lat + lon
                window.location.href = window.location.origin + window.location.pathname + 
                    "?nome=Cliente+GECOM" +
                    "&lat=" + sucesso.coords.latitude + 
                    "&lon=" + sucesso.coords.longitude;
            },
            function(erro) {
                let msg = "⚠️ Não conseguimos acessar sua localização\\n\\n";
                if (erro.code === 1) {
                    msg += "→ Toque no 🔒 CADEADO acima → Permitir localização\\n";
                    msg += "→ Depois toque no botão de novo";
                } else if (erro.code === 2) {
                    msg += "→ Sinal fraco — tente ao ar livre";
                } else {
                    msg += "→ Tente novamente";
                }
                alert(msg);
            },
            {enableHighAccuracy: true, timeout: 20000, maximumAge: 0}
        );
    }
    </script>
    """, height=230)

    st.info("💡 Toque uma vez → permita → a página recarrega sozinha")
    st.stop()

# ==================================================
# TELA 2 — DADOS RECEBIDOS → BOTÃO DE PÂNICO
# ==================================================
st.success("✅ DADOS E LOCALIZAÇÃO RECEBIDOS!")

# Mostra o nome junto
st.markdown(f"""
<div style='
    background:#fff0f0;
    border-left:5px solid #ff3333;
    padding:20px;
    border-radius:12px;
    margin:20px 0;
    font-size:18px;
    line-height:1.8;
'>
<strong style='font-size:20px;'>👤 Nome:</strong> {nome_usuario or "Cliente GECOM"}<br><br>
<strong style='font-size:20px;'>📍 Localização:</strong><br>{endereco_auto}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<h3 style='text-align:center;font-size:22px;margin:25px 0 15px;'>
🔴 Toque abaixo SOMENTE em caso de emergência
</h3>
""", unsafe_allow_html=True)

# === BOTÃO DE PÂNICO GIGANTE ===
if st.button("🚨 PÂNICO — EMERGÊNCIA", type="primary", use_container_width=True):
    with st.spinner("Enviando alerta à central..."):
        mapa_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        
        # Tenta sem acento primeiro
        dados = {
            "nome": nome_usuario or "CLIENTE GECOM",
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "lat": lat,
            "lon": lon,
            "endereco": endereco_auto,
            "obs": "EMERGÊNCIA — Usuário acionou botão de PÂNICO!",
            "mapa": mapa_link
        }
        
        resp = requests.post(API_URL, json=dados, headers=headers)
        
        if resp.status_code in [200, 201]:
            st.balloons()
            st.markdown(f"""
            <div style='
                background:linear-gradient(135deg,#ff0000,#880000);
                color:white;
                padding:35px 20px;
                border-radius:20px;
                text-align:center;
                margin:25px 0;
            '>
                <h2 style='font-size:28px;margin:0;'>✅ ALERTA ENVIADO!</h2>
                <p style='font-size:18px;margin:15px 0 0;'>Central foi notificada<br>Ajuda a caminho</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"🔗 **Ver localização no mapa:** [Clique aqui]({mapa_link})")
        else:
            # Tenta com acento se não funcionar
            dados["endereço"] = dados.pop("endereco")
            resp2 = requests.post(API_URL, json=dados, headers=headers)
            if resp2.status_code in [200, 201]:
                st.balloons()
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#ff0000,#880000);color:white;padding:35px;border-radius:20px;text-align:center;'>
                    <h2>✅ ALERTA ENVIADO!</h2>
                    <p>Central notificada</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"🔗 [Ver no mapa]({mapa_link})")
            else:
                st.error(f"❌ Erro: {resp.text[:250]}")

st.divider()

# === INSTALAÇÃO ===
st.markdown("""
### 📲 Instalar no celular
- **Android:** ⋮ → **Instalar app** ✅
- **iPhone:** ⬆️ → **Adicionar à Tela de Início** ✅
""")

st.caption("GECOM Segurança · Emergência: 190")
