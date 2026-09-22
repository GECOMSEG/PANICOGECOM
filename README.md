# =============================================
# GECOM SEGURANÇA — BOTÃO DE PÂNICO
# Versão final — sem banco, sem erros
# =============================================
import streamlit as st
from datetime import datetime

# ================== CONFIGURAÇÃO ==================
WHATSAPP_NUMERO = "5551998463372"  # ← SEU número
NOME_EMPRESA = "GECOM SEGURANÇA"
# ===================================================

st.set_page_config(page_title="🚨 Botão de Pânico", layout="centered")

# Tela principal
st.markdown("""
    <h1 style='text-align: center; color: red;'>🚨 BOTÃO DE PÂNICO</h1>
    <h4 style='text-align: center;'>{}</h4>
    <hr style='border: 2px solid red;'>
""".format(NOME_EMPRESA), unsafe_allow_html=True)

st.subheader("📍 Localização")
lat = st.text_input("Latitude")
lon = st.text_input("Longitude")

# Captura localização automatica
st.components.v1.html("""
<script>
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(pos => {
    setTimeout(() => {
      const inputs = window.parent.document.querySelectorAll('input');
      if (inputs.length>0) inputs[0].value = pos.coords.latitude.toFixed(7);
      if (inputs.length>1) inputs[1].value = pos.coords.longitude.toFixed(7);
    }, 300);
  });
}
</script>
""", height=0)

obs = st.text_area("📝 Detalhes (opcional)", placeholder="Nome, situação, endereço...")
st.divider()

# Botão de envio
if st.button("🚨 PEDIR SOCORRO AGORA", type="primary", use_container_width=True):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    local = f"{lat}, {lon}" if lat and lon else "Não disponível"
    mapa = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else ""
    
    mensagem = f"""🚨 ALERTA DE PÂNICO — {NOME_EMPRESA}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 Hora: {agora}
📍 Local: {local}
🗺️ Mapa: {mapa}
📝 Obs: {obs or 'Não informada'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ATENDIMENTO URGENTE SOLICITADO!
"""
    
    link_msg = mensagem.replace(" ", "%20").replace("\n", "%0A")
    link = f"https://wa.me/{WHATSAPP_NUMERO}?text={link_msg}"
    
    st.success("✅ ALERTA ENVIADO! Abrindo WhatsApp...")
    st.markdown(f"<a href='{link}' target='_blank'>👉 Clique aqui se não abrir</a>", unsafe_allow_html=True)
    st.code(mensagem, language=None)

st.divider()
st.info("💡 Salve o link na tela inicial do celular!")
