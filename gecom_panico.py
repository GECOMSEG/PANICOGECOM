import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="GECOM Pânico", layout="wide", initial_sidebar_state="expanded")

# =============================================
# BANCO COMPARTILHADO — TODOS VEEM OS MESMOS ALERTAS
# =============================================

# Inicializa banco centralizado
if "db_alertas" not in st.session_state:
    st.session_state.db_alertas = []

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

    nome = st.text_input("👤 Nome / Empresa")
    lat = st.text_input("📍 Latitude")
    lon = st.text_input("📍 Longitude")

    # Localização automática
    st.components.v1.html("""
    <script>
    if(navigator.geolocation){
      navigator.geolocation.getCurrentPosition(pos=>{
        setTimeout(()=>{
          const i=window.parent.document.querySelectorAll('input');
          if(i[1])i[1].value=pos.coords.latitude.toFixed(7);
          if(i[2])i[2].value=pos.coords.longitude.toFixed(7);
        },300);
      });
    }
    </script>
    """, height=0)

    endereco = st.text_input("🏠 Endereço / Referência")
    obs = st.text_area("📝 Situação")
    st.divider()

    if st.button("🚨 PEDIR SOCORRO AGORA", type="primary", use_container_width=True):
        if not nome:
            st.error("⚠️ Digite seu nome!")
        else:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tem_local = bool(lat and lon and lat.strip() and lon.strip())
            
            novo_alerta = {
                "nome": nome,
                "hora": agora,
                "lat": lat if tem_local else "Indisponível",
                "lon": lon if tem_local else "Indisponível",
                "endereco": endereco or "Não informado",
                "obs": obs or "Não informada",
                "mapa": f"https://www.google.com/maps?q={lat},{lon}" if tem_local else None
            }
            
            # Salva na base compartilhada
            st.session_state.db_alertas.insert(0, novo_alerta)
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()

# ========== TELA DA CENTRAL ==========
else:
    st.markdown("""
        <h1 style='text-align:center;color:green;'>📟 CENTRAL DE MONITORAMENTO</h1>
        <h3 style='text-align:center;'>GECOM SEGURANÇA — ALERTAS RECEBIDOS</h3>
        <hr style='border:2px solid green;'>
    """, unsafe_allow_html=True)

    # ⚠️ IMPORTANTE: Atualiza a página para buscar novos alertas
    st.rerun()

    # Pega alertas da base compartilhada
    alertas = st.session_state.db_alertas

    if not alertas:
        st.info("✅ Sistema online — Nenhum alerta recebido no momento")
    else:
        st.warning(f"⚠️ {len(alertas)} ALERTA(S) RECEBIDO(S)!")
        
        for numero, alerta in enumerate(alertas, 1):
            st.markdown(f"""
            <div style='background:#fff3cd;padding:15px;border-radius:8px;border-left:5px solid red;margin-bottom:12px;'>
            <h4>🚨 ALERTA #{numero}</h4>
            <p><strong>👤 Cliente:</strong> {alerta['nome']}</p>
            <p><strong>🕐 Hora:</strong> {alerta['hora']}</p>
            <p><strong>🏠 Endereço:</strong> {alerta['endereco']}</p>
            <p><strong>📍 Coordenadas:</strong> {alerta['lat']} / {alerta['lon']}</p>
            <p><strong>📝 Situação:</strong> {alerta['obs']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if alerta['mapa']:
                st.markdown(f"[🗺️ ABRIR MAPA → {alerta['nome']}]({alerta['mapa']})")
            st.divider()

    if st.button("🗑️ Limpar Todos os Alertas"):
        st.session_state.db_alertas = []
        st.rerun()
        
