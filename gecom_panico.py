import streamlit as st
from datetime import datetime

# =============================================
# GECOM — SISTEMA DE PÂNICO: CLIENTE + CENTRAL
# =============================================

st.set_page_config(page_title="GECOM Pânico", layout="wide")

# Armazena alertas
if "alertas" not in st.session_state:
    st.session_state.alertas = []

# ========== MENU LATERAL ==========
pagina = st.sidebar.radio("Acesso:", [
    "📲 Cliente — Enviar Alerta",
    "📟 Central — Receber Alertas"
])

# ========== TELA DO CLIENTE ==========
if pagina == "📲 Cliente — Enviar Alerta":
    st.markdown("""
        <h1 style='text-align:center;color:red;'>🚨 BOTÃO DE PÂNICO</h1>
        <h3 style='text-align:center;'>GECOM SEGURANÇA</h3>
        <hr style='border:2px solid red;'>
    """, unsafe_allow_html=True)

    nome = st.text_input("👤 Seu Nome / Razão Social")
    lat = st.text_input("📍 Latitude")
    lon = st.text_input("📍 Longitude")

    # Pega localização automática
    st.components.v1.html("""
    <script>
    if(navigator.geolocation){
      navigator.geolocation.getCurrentPosition(pos=>{
        setTimeout(()=>{
          const i = window.parent.document.querySelectorAll('input');
          if(i[1])i[1].value = pos.coords.latitude.toFixed(7);
          if(i[2])i[2].value = pos.coords.longitude.toFixed(7);
        }, 300);
      });
    }
    </script>
    """, height=0)

    endereco = st.text_input("🏠 Endereço / Ponto de Referência")
    obs = st.text_area("📝 Descrição da Situação", placeholder="O que está acontecendo?")

    st.divider()

    if st.button("🚨 PEDIR SOCORRO AGORA", type="primary", use_container_width=True):
        if not nome:
            st.error("⚠️ Digite seu nome!")
        else:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tem_local = lat and lon and lat.strip() and lon.strip()
            
            alerta = {
                "nome": nome,
                "hora": agora,
                "lat": lat if tem_local else "Não disponível",
                "lon": lon if tem_local else "Não disponível",
                "endereco": endereco or "Não informado",
                "obs": obs or "Não informada",
                "mapa": f"https://www.google.com/maps?q={lat},{lon}" if tem_local else None
            }
            
            st.session_state.alertas.insert(0, alerta)
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()

# ========== TELA DA CENTRAL ==========
else:
    st.markdown("""
        <h1 style='text-align:center;color:green;'>📟 CENTRAL DE MONITORAMENTO</h1>
        <h3 style='text-align:center;'>GECOM SEGURANÇA — ALERTAS RECEBIDOS</h3>
        <hr style='border:2px solid green;'>
    """, unsafe_allow_html=True)

    # Atualiza a página para mostrar novos alertas
    st.rerun()

    if not st.session_state.alertas:
        st.info("✅ Sistema online — Nenhum alerta recebido no momento")
    else:
        st.warning(f"⚠️ {len(st.session_state.alertas)} ALERTA(S) RECEBIDO(S)!")
        
        for num, a in enumerate(st.session_state.alertas, 1):
            st.markdown(f"""
            <div style='background:#fff3cd;padding:15px;border-radius:8px;border-left:5px solid red;'>
            <h4>🚨 ALERTA #{num}</h4>
            <p><strong>Cliente:</strong> {a['nome']}</p>
            <p><strong>Hora:</strong> {a['hora']}</p>
            <p><strong>Endereço:</strong> {a['endereco']}</p>
            <p><strong>Coordenadas:</strong> {a['lat']} / {a['lon']}</p>
            <p><strong>Observação:</strong> {a['obs']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if a['mapa']:
                st.markdown(f"[🗺️ ABRIR MAPA → {a['nome']}]({a['mapa']})")
            st.divider()

    if st.button("🗑️ Limpar Todos os Alertas"):
        st.session_state.alertas = []
        st.rerun()
            
