import streamlit as st
import requests
from datetime import datetime

# === DADOS DO SEU PROJETO ===
API_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1/alertas"
CHAVE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"
# =============================

st.set_page_config(page_title="GECOM Alerta Panico", page_icon="🚨", layout="centered")

st.markdown("""
<style>
h1 {color: #cc0000; text-align: center;}
div.stButton > button {background-color: #cc0000; color: white; font-size: 22px; height: 80px; width: 100%; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🚨 ALERTA DE PANICO — GECOM SEGURANCA")
st.subheader("Protecao Maxima")
st.divider()

nome = st.text_input("Seu Nome / Identificacao")
col1, col2 = st.columns(2)
with col1:
    lat = st.text_input("Latitude")
with col2:
    lon = st.text_input("Longitude")
endereco = st.text_input("Endereco / Referencia")
obs = st.text_area("Observacoes")

if st.button("🚨 ENVIAR ALERTA AGORA", type="primary"):
    if not nome:
        st.error("⚠️ Digite seu nome!")
    else:
        with st.spinner("Enviando alerta..."):
            hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            mapa_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
            
            dados = {
                "nome": nome,
                "hora": hora_atual,
                "lat": lat,
                "lon": lon,
                "endereco": endereco,
                "obs": obs,
                "mapa": mapa_link
            }
            
            cabecalhos = {
                "apikey": CHAVE,
                "Authorization": f"Bearer {CHAVE}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            
            resp = requests.post(API_URL, json=dados, headers=cabecalhos)
            
            if resp.status_code in (200, 201):
                st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
                st.info(f"Nome: {nome}\nHora: {hora_atual}\nEndereco: {endereco or 'Nao informado'}")
                if mapa_link:
                    st.markdown(f"[📍 Ver no Mapa]({mapa_link})")
            else:
                st.error(f"❌ Erro {resp.status_code}: {resp.text}")

st.divider()
st.caption("GECOM Seguranca — Protecao Maxima · Emergencia: 190")
