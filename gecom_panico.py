import streamlit as st
from datetime import datetime

st.set_page_config(page_title="GECOM Pânico", layout="wide")

# Armazenamento compartilhado
if "alertas" not in st.session_state:
    st.session_state.alertas = []

# ========== MENU LATERAL ==========
pagina = st.sidebar.radio("Escolha:", [
    "📲 ENVIAR ALERTA (Cliente)",
    "📟 RECEBER ALERTAS (Central)"
])

# ========== TELA DO CLIENTE ==========
if pagina == "📲 ENVIAR ALERTA (Cliente)":
    st.markdown("<h1 style='text-align:center;color:red;'>🚨 BOTÃO DE PÂNICO</h1>", unsafe_allow_html=True)
    st.subheader("GECOM SEGURANÇA")
    st.divider()

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

    endereco = st.text_input("🏠 Endereço")
    obs = st.text_area("📝 Situação")
    st.divider()

    if st.button("🚨 PEDIR SOCORRO AGORA", type="primary", use_container_width=True):
        if not nome:
            st.error("Digite seu nome!")
        else:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tem_local = bool(lat and lon and lat.strip() and lon.strip())
            
            alerta = {
                "nome": nome,
                "hora": agora,
                "lat": lat if tem_local else "Indisponível",
                "lon": lon if tem_local else "Indisponível",
                "endereco": endereco or "Não informado",
                "obs": obs or "Não informada",
                "mapa": f"https://www.google.com/maps?q={lat},{lon}" if tem_local else None
            }
            
            st.session_state.alertas.insert(0, alerta)
            st.success("✅ ENVIADO PARA A CENTRAL!")
            st.balloons()

# ========== TELA DA CENTRAL ==========
else:
    st.markdown("<h1 style='text-align:center;color:green;'>📟 CENTRAL DE MONITORAMENTO</h1>", unsafe_allow_html=True)
    st.subheader("GECOM SEGURANÇA — ALERTAS RECEBIDOS")
    st.divider()

    st.rerun()  # Atualiza automaticamente

    if not st.session_state.alertas:
        st.info("✅ Sistema operacional — Nenhum alerta no momento")
    else:
        st.warning(f"⚠️ {len(st.session_state.alertas)} ALERTA(S)!")
        for n, a in enumerate(st.session_state.alertas, 1):
            st.markdown(f"""
            <div style='background:#fff3cd;padding:12px;border-radius:8px;border-left:5px solid red;'>
            <h4>🚨 ALERTA #{n}</h4>
            <p><strong>Cliente:</strong> {a['nome']}</p>
            <p><strong>Hora:</strong> {a['hora']}</p>
            <p><strong>Endereço:</strong> {a['endereco']}</p>
            <p><strong>Coordenadas:</strong> {a['lat']} / {a['lon']}</p>
            <p><strong>Obs:</strong> {a['obs']}</p>
            </div>
            """, unsafe_allow_html=True)
            if a['mapa']:
                st.markdown(f"[🗺️ ABRIR MAPA]({a['mapa']})")
            st.divider()

    if st.button("🗑️ Limpar Lista"):
        st.session_state.alertas = []
        st.rerun()
        
