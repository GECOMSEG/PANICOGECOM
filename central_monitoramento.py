import streamlit as st
import requests
from datetime import datetime

# === DADOS EXATOS DO SEU PROJETO ===
API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"
# ====================================

st.set_page_config(page_title="CENTRAL — GECOM", page_icon="🚨", layout="wide")

st.markdown("""
<style>
h1 {color: #cc0000; text-align: center;}
.card {padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid;}
.verde {background: #e8f5e9; border-color: #4caf50;}
.amarelo {background: #fff8e1; border-color: #ff9800;}
.vermelho {background: #ffebee; border-color: #f44336;}
</style>
""", unsafe_allow_html=True)

st.title("🚨 CENTRAL DE MONITORAMENTO — GECOM SEGURANÇA")
st.subheader("Proteção Máxima · Campo Bom / RS")
st.divider()

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}"
}

try:
    resp = requests.get(f"{API_URL}?order=id.desc&limit=50", headers=headers)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Atualizar"):
            st.rerun()
    with col2:
        st.info(f"Última verificação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    st.divider()
    
    if resp.status_code == 200:
        alertas = resp.json()
        
        if not alertas:
            st.success("✅ Conectado! Nenhum alerta recebido ainda.")
        else:
            st.subheader(f"📋 {len(alertas)} Alerta(s) Recebido(s)")
            for a in alertas:
                obs = (a.get("obs") or "").lower()
                cor = "vermelho" if any(p in obs for p in ["perigo", "emergência", "roubo", "pânico"]) else "amarelo"
                st.markdown(f"<div class='card {cor}'>", unsafe_allow_html=True)
                st.markdown(f"### 🚨 {a.get('hora', '—')}")
                st.markdown(f"**👤 Nome:** {a.get('nome', '—')}")
                st.markdown(f"**📍 Endereço:** {a.get('endereco') or 'Não informado'}")
                if a.get("lat") and a.get("lon") and a["lat"] and a["lon"]:
                    lat, lon = a["lat"], a["lon"]
                    st.markdown(f"**📌 Mapa:** [Abrir no Google Maps](https://www.google.com/maps/search/?api=1&query={lat},{lon})")
                if a.get("obs"):
                    st.markdown(f"**📝 Observações:** {a['obs']}")
                st.markdown("</div>", unsafe_allow_html=True)
                st.divider()
    else:
        st.error(f"❌ Erro {resp.status_code}: {resp.text}")

except Exception as e:
    st.error(f"❌ Falha: {str(e)}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
        
