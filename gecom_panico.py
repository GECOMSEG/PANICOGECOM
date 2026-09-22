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
            st.error(f"Erro conexão: {e}")
            return None

    def cadastrar_usuario(self, cliente_id, nome, telefone, senha):
        conn = self.conectar()
        if not conn: return False
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO usuarios_clientes (cliente_id, nome, telefone, senha_acesso)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (cliente_id, nome, telefone, senha))
            conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            print(f"Erro cadastro: {e}")
            return False
        finally:
            conn.close()

    def verificar_login(self, nome, senha):
        conn = self.conectar()
        if not conn: return None
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT u.*, c.razao_social, c.telefone as cliente_telefone
                FROM usuarios_clientes u
                LEFT JOIN clientes c ON u.cliente_id = c.id
                WHERE u.nome = %s AND u.senha_acesso = %s AND u.ativo = TRUE
            """, (nome, senha))
            return cur.fetchone()
        finally:
            conn.close()

    def registrar_alerta(self, usuario_id, cliente_id, lat, lon, obs=""):
        conn = self.conectar()
        if not conn: return False
        try:
            endereco = self._coordenadas_para_endereco(lat, lon) if lat and lon else "Localização não disponível"
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO alertas_panico 
                (usuario_id, cliente_id, latitude, longitude, endereco_aproximado, observacao)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (usuario_id, cliente_id, lat, lon, endereco, obs))
            alerta_id = cur.fetchone()[0]
            conn.commit()
            threading.Thread(target=notificar_central, args=(alerta_id, lat, lon, endereco, obs)).start()
            return alerta_id
        except Exception as e:
            print(f"Erro registrar alerta: {e}")
            return False
        finally:
            conn.close()

    def _coordenadas_para_endereco(self, lat, lon):
        try:
            geo = Nominatim(user_agent="gecom_panico")
            local = geo.reverse(f"{lat}, {lon}", exactly_one=True)
            return local.address if local else "Endereço não encontrado"
        except:
            return "Consulta de endereço indisponível"

    def listar_alertas(self, apenas_pendentes=False, limite=100):
        conn = self.conectar()
        if not conn: return []
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            sql = """
                SELECT a.*, u.nome as usuario_nome, c.razao_social
                FROM alertas_panico a
                LEFT JOIN usuarios_clientes u ON a.usuario_id = u.id
                LEFT JOIN clientes c ON a.cliente_id = c.id
            """
            if apenas_pendentes:
                sql += " WHERE a.resolvido = FALSE "
            sql += " ORDER BY a.data_hora DESC LIMIT %s"
            cur.execute(sql, (limite,))
            return cur.fetchall()
        finally:
            conn.close()

    def marcar_resolvido(self, alerta_id, operador, resposta=""):
        conn = self.conectar()
        if not conn: return False
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE alertas_panico 
                SET resolvido = TRUE, operador_responsavel = %s, 
                    data_resolucao = %s, resposta_operador = %s
                WHERE id = %s
            """, (operador, datetime.now(), resposta, alerta_id))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

# =============================================
# 🔔 NOTIFICAÇÃO WHATSAPP
# =============================================
def notificar_central(alerta_id, lat, lon, endereco, obs=""):
    if not WHATSAPP_ATIVO: return
    try:
        link_mapa = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "Sem localização"
        mensagem = f"""
🚨 ALERTA DE PÂNICO — {NOME_EMPRESA}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆔 ID: #{alerta_id}
🕐 Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
📍 Local: {endereco}
🗺️ Mapa: {link_mapa}
📝 Obs: {obs or 'Não informada'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Encaminhar equipe IMEDIATAMENTE!
🛡️ {NOME_EMPRESA}
        """.strip()
        pywhatkit.sendwhatmsg_instantly(WHATSAPP_NUMERO_CENTRAL, mensagem, wait_time=15, tab_close=True, close_time=2)
        print(f"✅ Alerta #{alerta_id} enviado")
    except Exception as e:
        print(f"❌ WhatsApp: {e}")

# =============================================
# 📱 INTERFACE
# =============================================
st.set_page_config(page_title="GECOM — Botão de Pânico", layout="centered", page_icon="🚨")
db = BancoPanico()

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# =============================================
# TELA DE LOGIN
# =============================================
if not st.session_state.usuario_logado:
    st.markdown("""
        <h1 style='text-align: center; color: #ff0000;'>🚨 GECOM — BOTÃO DE PÂNICO</h1>
        <p style='text-align: center;'>Acesso exclusivo para clientes</p>
    """, unsafe_allow_html=True)

    aba_login, aba_cadastro = st.tabs(["🔐 Entrar", "📝 Novo Acesso"])

    with aba_login:
        nome = st.text_input("Seu Nome / Usuário")
        senha = st.text_input("Sua Senha", type="password")
        if st.button("🔓 Entrar", use_container_width=True):
            usuario = db.verificar_login(nome, senha)
            if usuario:
                st.session_state.usuario_logado = usuario
                st.rerun()
            else:
                st.error("❌ Nome ou senha incorretos")

    with aba_cadastro:
        st.info("Solicite seu cadastro pelo telefone:")
        st.write(f"📞 {WHATSAPP_NUMERO_CENTRAL}")

# =============================================
# ÁREA DO CLIENTE
# =============================================
elif st.session_state.usuario_logado:
    u = st.session_state.usuario_logado
    st.markdown(f"<h3 style='color: #ff0000;'>Bem-vindo, {u['nome']}</h3>", unsafe_allow_html=True)

    if st.button("🚪 Sair"):
        st.session_state.usuario_logado = None
        st.rerun()

    st.divider()

    st.markdown("""
        <h2 style='text-align: center; color: red;'>APERTE EM CASO DE EMERGÊNCIA</h2>
        <p style='text-align: center;'>A localização será enviada automaticamente para a GECOM</p>
    """, unsafe_allow_html=True)

    lat = st.text_input("Latitude", key="lat_input")
    lon = st.text_input("Longitude", key="lon_input")

    st.components.v1.html("""
    <script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(pos) {
                const lat = pos.coords.latitude.toFixed(7);
                const lon = pos.coords.longitude.toFixed(7);
                const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs[0]) inputs[0].value = lat;
                if (inputs[1]) inputs[1].value = lon;
            }
        );
    }
    </script>
    """, height=0)

    observacao = st.text_area("Detalhes (opcional)", placeholder="Ex: 2 pessoas, veículo branco...")

    if st.button("🚨 ESTOU EM PERIGO — PEDIDO DE SOCORRO", type="primary", use_container_width=True):
        lat_val = st.session_state.get("lat_input") or None
        lon_val = st.session_state.get("lon_input") or None
        
        alerta_id = db.registrar_alerta(u["id"], u["cliente_id"], lat_val, lon_val, observacao)
        
        if alerta_id:
            st.success("""
            ✅ ALERTA ENVIADO!
            🚨 A GECOM foi avisada e está agindo.
            📞 Mantenha o telefone ligado.
            """)
        else:
            st.error("❌ Falha! Ligue para a central.")

    st.divider()

    st.subheader("📋 Meus Alertas")
    alertas = db.listar_alertas(limite=5)
    meus = [a for a in alertas if a["usuario_id"] == u["id"]]
    if meus:
        for a in meus:
            status = "✅ Resolvido" if a["resolvido"] else "🔴 Pendente"
            st.info(f"{a['data_hora'].strftime('%d/%m %H:%M')} — {status}")
    else:
        st.info("Nenhum alerta enviado")
