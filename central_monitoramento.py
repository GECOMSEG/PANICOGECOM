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

# ESTILO
st.markdown("""
<style>
h1 {color: #cc0000; text-align: center;}
h2 {color: #2c3e50;}
.alerta-novo {background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 8px; margin: 10px 0;}
.alerta-perigo {background-color: #f8d7da; border-left: 5px solid #dc3545; padding: 15px; border-radius: 8px; margin: 10px 0;}
.alerta-normal {background-color: #d1e7dd; border-left: 5px solid #198754; padding: 15px; border-radius: 8px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.title("🚨 CENTRAL DE MONITORAMENTO — GECOM SEGURANÇA")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

# FUNÇÃO PARA BUSCAR ALERTAS
def buscar_alertas():
    cabecalhos = {
        "apikey": CHAVE,
        "Authorization": f"Bearer {CHAVE}",
        "Content-Type": "application/json"
    }
    # Pega os últimos 50 alertas, do mais novo ao mais antigo
    params = {"order": "id.desc", "limit": 50}
    try:
        resp = requests.get(API_URL, headers=cabecalhos, params=params)
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        st.error(f"Erro ao buscar: {e}")
        return []

# BOTÃO DE ATUALIZAR
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 Atualizar"):
        st.rerun()
with col2:
    st.info("Última atualização: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

st.divider()

# LISTA DE ALERTAS
alertas = buscar_alertas()

if not alertas:
    st.success("✅ Nenhum alerta recebido até o momento. Sistema funcionando!")
else:
    st.subheader(f"📋 {len(alertas)} Alerta(s) Recebido(s)")
    
    for alerta in alertas:
        # Define cor do card
        obs = (alerta.get("obs") or "").lower()
        classe = "alerta-perigo" if any(p in obs for p in ["perigo", "emergência", "ataque", "roubo", "pânico"]) else "alerta-novo"
        
        with st.container():
            st.markdown(f'<div class="{classe}">', unsafe_allow_html=True)
            
            st.markdown(f"### 🚨 Alerta — {alerta.get('hora', 'Sem horário')}")
            st.markdown(f"**👤 Responsável:** {alerta.get('nome', 'Não informado')}")
            
            if alerta.get("endereco"):
                st.markdown(f"**📍 Local:** {alerta['endereco']}")
            
            if alerta.get("lat") and alerta.get("lon"):
                lat = alerta["lat"]
                lon = alerta["lon"]
                st.markdown(f"**📌 Coordenadas:** {lat}, {lon}")
                st.markdown(f"[👉 Ver no Mapa — Google Maps](https://www.google.com/maps/search/?api=1&query={lat},{lon})")
            
            if alerta.get("obs"):
                st.markdown(f"**📝 Observações:** {alerta['obs']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.divider()

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
