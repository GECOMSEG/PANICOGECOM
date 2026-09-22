import streamlit as st
from datetime import datetime

WHATSAPP_NUMERO = "5551998463372"
NOME_EMPRESA = "GECOM SEGURANÇA"

st.set_page_config(page_title="Botão de Pânico", layout="centered")

st.markdown("<h1 style='text-align:center;color:red;'>🚨 BOTÃO DE PÂNICO</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;'>{NOME_EMPRESA}</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border:2px solid red;'>", unsafe_allow_html=True)

lat = st.text_input("Latitude")
lon = st.text_input("Longitude")

st.components.v1.html("""
<script>
if(navigator.geolocation){
  navigator.geolocation.getCurrentPosition(pos=>{
    setTimeout(()=>{
      const i=window.parent.document.querySelectorAll('input');
      if(i[0])i[0].value=pos.coords.latitude.toFixed(7);
      if(i[1])i[1].value=pos.coords.longitude.toFixed(7);
    },300);
  });
}
</script>
""", height=0)

obs = st.text_area("Detalhes", placeholder="Nome, situação...")

if st.button("🚨 PEDIR SOCORRO", type="primary", use_container_width=True):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    local = f"{lat}, {lon}" if lat and lon else "Não disponível"
    mapa = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else ""
    
    msg = f"""🚨 ALERTA DE PÂNICO — {NOME_EMPRESA}
Hora: {agora}
Local: {local}
Mapa: {mapa}
Obs: {obs or 'Não informada'}
SOLICITA ATENDIMENTO URGENTE!"""
    
    link_msg = msg.replace(" ","%20").replace("\n","%0A")
    link = f"https://wa.me/{WHATSAPP_NUMERO}?text={link_msg}"
    
    st.success("✅ ALERTA ENVIADO!")
    st.markdown(f"<a href='{link}' target='_blank'>Abrir WhatsApp</a>", unsafe_allow_html=True)
    st.code(msg)

st.info("Salve o link na tela inicial do celular!")
