import streamlit as st
import requests
from datetime import datetime

# === DADOS DO SEU PROJETO ===
API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t21VYcgneOXD93PW5GcnQ_BisRaVZS"
# =============================

st.set_page_config(
    page_title="CENTRAL — GECOM Segurança",
    page_icon="🚨",
    layout="wide"
)

st.markdown("""
<style>
h1 {color: #cc0000; text-align: center;}
.caixa {padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid;}
.novo {background: #fff8e1; border-color: #ff9800;}
.normal {background: #e8f5e9; border-color: #4caf50;}
.perigo {background: #ffebee; border-color: #f44336;}
</style>
""", unsafe_allow_html=True)

st.title("🚨 CENTRAL DE MONITORAMENTO — GECOM SEGURANÇA")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

def buscar_alertas():
    headers = {
        "apikey": CHAVE,
        "Authorization": f"Bearer {CHAVE}"
    }
    try:
        r = requests.get(f"{API_URL}?order=id.desc&limit=50", headers=headers)
        return r.json() if r.status_code == 200 else []
    except:
        return []

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Atualizar"):
        st.rerun()
with col2:
    st.info(f"Última verificação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

st.divider()

alertas = buscar_alertas()

if not alertas:
    st.success("✅ Nenhum alerta recebido. Sistema funcionando perfeitamente!")
else:
    st.subheader(f"📋 {len(alertas)} Alerta(s) Registrado(s)")
    
    for a in alertas:
        obs = (a.get("obs") or "").lower()
        classe = "perigo" if any(p in obs for p in ["perigo", "emergência", "roubo", "pânico"]) else "novo"
        
        st.markdown(f"<div class='caixa {classe}'>", unsafe_allow_html=True)
        st.markdown(f"### 🚨 {a.get('hora', 'Sem data')}")
        st.markdown(f"**👤 Nome:** {a.get('nome', '—')}")
        
        if a.get("endereco"):
            st.markdown(f"**📍 Endereço:** {a['endereco']}")
        
        if a.get("lat") and a.get("lon") and a["lat"] and a["lon"]:
            lat, lon = a["lat"], a["lon"]
            st.markdown(f"**📌 Localização:** [{lat}, {lon}](https://www.google.com/maps/search/?api=1&query={lat},{lon})")
        else:
            st.markdown("**📌 Localização:** Não informada")
        
        if a.get("obs"):
            st.markdown(f"**📝 Observações:** {a['obs']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
