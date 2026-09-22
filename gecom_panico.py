"
import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# DADOS DO SUPABASE
SUPABASE_URL = "https://hbyqdrewpztjupyulyts.supabase.co"
SUPABASE_KEY = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS
# CONEXÃO
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GECOM — Alerta de Pânico", page_icon="🚨", layout="centered")

st.markdown("""
<style>
h1 {color: #cc0000; text-align: center;}
div.stButton > button {background-color: #cc0000; color: white; font-size: 22px; height: 80px; width: 100%; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🚨 ALERTA DE PÂNICO — GECOM SEGURANÇA")
st.subheader("Proteção Máxima")
st.divider()

# FORMULÁRIO
nome = st.text_input("Seu Nome / Identificação")
col1, col2 = st.columns(2)
with col1:
    lat = st.text_input("Latitude")
with col2:
    lon = st.text_input("Longitude")
endereco = st.text_input("Endereço / Referência")
obs = st.text_area("Observações")

# BOTÃO DE ENVIO
if st.button("🚨 ENVIAR ALERTA AGORA", type="primary"):
    if not nome:
        st.error("⚠️ Digite seu nome!")
    else:
        hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mapa_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        
        # SALVAR NO BANCO
        dados = {
            "nome": nome,
            "hora": hora_atual,
            "lat": lat,
            "lon": lon,
            "endereco": endereco,
            "obs": obs,
            "mapa": mapa_link
        }
        
        resposta = supabase.table("alertas").insert(dados).execute()
        
        st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
        st.info(f"""
        📋 **Dados enviados:**
        - Nome: {nome}
        - Hora: {hora_atual}
        - Endereço: {endereco or "Não informado"}
        """)
        if mapa_link:
            st.markdown(f"[📍 Ver no Mapa]({mapa_link})")

st.divider()
st.caption("GECOM Segurança — Proteção Máxima · Emergência: 190")
