# =============================================
# GECOM SEGURANÇA — BOTÃO DE PÂNICO
# Versão simplificada: funciona no Streamlit Cloud
# =============================================
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# Configurações
WHATSAPP_NUMERO = "5551998463372"  # ← TROQUE pelo SEU número
NOME_EMPRESA = "GECOM SEGURANÇA"

st.set_page_config(page_title="🚨 Botão de Pânico — GECOM", layout="centered")

# Tela principal
st.markdown("""
    <h1 style='text-align: center; color: red;'>🚨 BOTÃO DE PÂNICO</h1>
    <h3 style='text-align: center;'>{}</h3>
""".format(NOME_EMPRESA), unsafe_allow_html=True)

st.divider()

# Captura de localização
components.html("""
<script>
navigator.geolocation.getCurrentPosition(
    pos => {
        const lat = pos.coords.latitude.toFixed(7);
        const lon = pos.coords.longitude.toFixed(7);
        window.parent.document.querySelector('[data-testid="stTextInput"] input:nth-child(1)').value = lat;
        window.parent.document.querySelectorAll('[data-testid="stTextInput"] input:nth-child(2)').value = lon;
    },
    err => console.log("Localização não disponível")
);
</script>
""", height=0)

lat = st.text_input("Latitude", key="lat_fixo")
lon = st.text_input("Longitude", key="lon_fixo")
observacao = st.text_area("Detalhes adicionais", placeholder="Nome, endereço, situação...", height=100)

st.divider()

# Botão de envio
if st.button("🚨 ENVIAR ALERTA DE PÂNICO", type="primary", use_container_width=True):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    localizacao = f"{lat}, {lon}" if lat and lon else "Não obtida"
    mapa = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else ""
    
    mensagem = f"""🚨 ALERTA DE PÂNICO — {NOME_EMPRESA}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Data/Hora: {agora}
📍 Localização: {localizacao}
🗺️ Mapa: {mapa}
📝 Observação: {observacao or 'Não informada'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ATENÇÃO — Solicita-se atendimento imediato!
"""
    
    # Codifica mensagem para link do WhatsApp
    link_mensagem = mensagem.replace(" ", "%20").replace("\n", "%0A")
    link_whatsapp = f"https://wa.me/{WHATSAPP_NUMERO}?text={link_mensagem}"
    
    st.success("✅ ALERTA ENVIADO! Abrindo WhatsApp...")
    st.markdown(f"""
        <meta http-equiv="refresh" content="1; url={link_whatsapp}">
        <p style='text-align:center; font-size:18px;'>
            Se não abrir automaticamente → 
            <a href='{link_whatsapp}' target='_blank'>Clique AQUI</a>
        </p>
    """, unsafe_allow_html=True)
    
    st.code(mensagem, language=None)

st.divider()
st.info("💡 Dica: Salve este atalho na tela inicial do celular como aplicativo!")
