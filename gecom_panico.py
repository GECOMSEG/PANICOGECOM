import streamlit as st
from datetime import datetime

# =============================================
# SISTEMA DE PÂNICO GECOM — CLIENTE + CENTRAL
# =============================================

st.set_page_config(page_title="GECOM — Pânico", layout="wide")

# 🔐 ÁREA DE DADOS COMPARTILHADOS
# Usamos a sessão para guardar os alertas
if "alertas" not in st.session_state:
    st.session_state.alertas = []

# ========== ESCOLHA DE TELA ==========
tela = st.sidebar.radio("Selecionar Tela:", [
    "📲 Cliente — Botão de Pânico",
    "📟 Central — Monitoramento"
])

# ========== TELA DO CLIENTE ==========
if tela == "📲 Cliente — Botão de Pânico":
    
    st.markdown("""
        <h1 style='text-align:center;color:red;'>🚨 BOTÃO DE PÂNICO</h1>
        <h3 style='text-align:center;'>GECOM SEGURANÇA</h3>
        <hr style='border:2px solid red;'>
    """, unsafe_allow_html=True)

    nome_cliente = st.text_input("👤 Seu Nome / Empresa")
    lat = st.text_input("📍 Latitude")
    lon = st.text_input("📍 Longitude")

    # Pegar localização automática
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

    endereco = st.text_input("🏠 Endereço / Referência")
    descricao = st.text_area("📝 Situação", placeholder="Descreva o que está acontecendo...")

    st.divider()

    if st.button("🚨 PEDIR SOCORRO — URGENTE", type="primary", use_container_width=True):
        if not nome_cliente:
            st.error("⚠️ Digite seu nome!")
        else:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tem_local = lat and lon and lat.strip() and lon.strip()
            
            novo_alerta = {
                "nome": nome_cliente,
                "data": agora,
                "lat": lat if tem_local else "Não disponível",
                "lon": lon if tem_local else "Não disponível",
                "endereco": endereco or "Não informado",
                "descricao": descricao or "Não informada",
                "mapa": f"https://www.google.com/maps?q={lat},{lon}" if tem_local else None
            }
            
            # Adiciona na lista (aparece na Central)
            st.session_state.alertas.insert(0, novo_alerta)
            
            st.success("✅ ALERTA ENVIADO PARA A CENTRAL!")
            st.balloons()
            
            st.markdown(f"""
            <div style='background:#ffebee;padding:15px;border-radius:10px;border:2px solid red;'>
            <h3>📤 Mensagem enviada:</h3>
            <p><strong>De:</strong> {nome_cliente}</p>
            <p><strong>Hora:</strong> {agora}</p>
            <p><strong>Local:</strong> {endereco or 'Ver mapa'}</p>
            </div>
            """, unsafe_allow_html=True)

    st.info("💡 Salve este link na tela inicial do celular! Permita a localização!")

# ========== TELA DA CENTRAL ==========
else:
    st.markdown("""
        <h1 style='text-align:center;color:#2E7D32;'>📟 CENTRAL DE MONITORAMENTO</h1>
        <h3 style='text-align:center;'>GECOM SEGURANÇA — ALERTAS DE PÂNICO</h3>
        <hr style='border:2px solid green;'>
    """, unsafe_allow_html=True)

    # Atualização automática
    st.rerun()

    if not st.session_state.alertas:
        st.info("✅ Nenhum alerta recebido — Sistema operacional")
    else:
        total = len(st.session_state.alertas)
        st.warning(f"⚠️ {total} ALERTA(S) RECEBIDO(S)!")
        
        for idx, alerta in enumerate(st.session_state.alertas):
            with st.container():
                st.markdown(f"""
                <div style='background:#fff3cd;padding:15px;border-radius:8px;border-left:5px solid orange;'>
                <h4>🚨 ALERTA #{idx+1}</h4>
                <p><strong>👤 Cliente:</strong> {alerta['nome']}</p>
                <p><strong>🕐 Hora:</strong> {alerta['data']}</p>
                <p><strong>🏠 Endereço:</strong> {alerta['endereco']}</p>
                <p><strong>📍 Coordenadas:</strong> {alerta['lat']} / {alerta['lon']}</p>
                <p><strong>📝 Situação:</strong> {alerta['descricao']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if alerta['mapa']:
                    st.markdown(f"[🗺️ ABRIR MAPA → {alerta['nome']}]({alerta['mapa']})")
                
                st.divider()

    if st.button("🗑️ Limpar Alertas"):
        st.session_state.alertas = []
        st.rerun()
  
