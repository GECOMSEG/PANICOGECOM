import streamlit as st
import requests
from datetime import datetime

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

# === URL CERTA — COPIADA DO SEU SUPABASE ===
API_URL = "Project URL: https://hbyqdwepwzpjupzyukyts.supabase.co"
"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"
# ===========================================

headers = {
    "apikey": CHAVE,
    "Authorization": f"Bearer {CHAVE}"
}

try:
    resp = requests.get(f"{API_URL}?order=id.desc&limit=50", headers=headers)
    
    if resp.status_code == 200:
        alertas = resp.json()
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Atualizar"):
                st.rerun()
        with col2:
            st.info(f"Última verificação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        st.divider()
        
        if not alertas:
            st.warning("⚠️ Conectado! Nenhum alerta registrado ainda.")
        else:
            st.success(f"✅ {len(alertas)} Alerta(s) Recebido(s)!")
            for a in alertas:
                nome = a.get("nome") or "Não informado"
                hora = a.get("hora") or "—"
                endereco = a.get("endereço") or "Não informado"
                lat = a.get("lat")
                lon = a.get("lon")
                obs = (a.get("obs") or "").lower()
                mapa = a.get("mapa")
                
                cor = "vermelho" if any(p in obs for p in ["perigo", "emergência", "roubo", "pânico"]) else "amarelo"
                
                st.markdown(f"<div class='card {cor}'>", unsafe_allow_html=True)
                st.markdown(f"### 🚨 {hora}")
                st.markdown(f"**👤 Nome:** {nome}")
                st.markdown(f"**📍 Endereço:** {endereco}")
                
                if lat and lon and lat != "EMPTY" and lon != "EMPTY":
                    st.markdown(f"**📌 Localização:** [Abrir no Google Maps](https://www.google.com/maps/search/?api=1&query={lat},{lon})")
                elif mapa:
                    st.markdown(f"**📌 Mapa:** {mapa}")
                
                if obs:
                    st.markdown(f"**📝 Observações:** {obs}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.divider()
    else:
        st.error(f"❌ Erro {resp.status_code}: {resp.text}")

except Exception as e:
    st.error(f"❌ Falha: {str(e)}")

st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
