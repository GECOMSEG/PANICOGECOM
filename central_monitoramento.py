import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="GECOM — Monitoramento", page_icon="🚨", layout="centered")

SUPABASE_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1"
CHAVE_SUPABASE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"

# === PWA + NOTIFICAÇÕES — AGORA PEDINDO PERMISSÃO ===
st.components.v1.html("""
<meta name="theme-color" content="#ff0000">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

<!-- Manifesto para instalar como app -->
<link rel="manifest" href="data:application/manifest+json;base64,eyJuYW1lIjoiR0VDT00gU2VndXJhbmNhIiwic2hvcnRfbmFtZSI6IkdFQ09NIiwiZGVzY3JpcHRpb24iOiJQcm90ZcOtc2EgTWF4aW1hIiwiZGVzaWduX3Njb3BlIjoiLyIsInN0YXJ0X3VybCI6Ii8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImJhY2tncm91bmRfY29sb3IiOiIjMGUwMDAwIiwidGhlbWVfY29sb3IiOiNmZjAwMDAiLCJpY29ucyI6W3sic3JjIjoiaHR0cHM6Ly92aWEucGxhY2Vob2xkZXIuY29tLzE5Mi9GRjAwMDAvRkZGRkZGIT90ZXh0PUciLCJzaXplcyI6IjE5MnwxOTIiLCJ0eXBlIjoiaW1hZ2UvcG5nIn1dfQ==">

<script>
async function pedirPermissao() {
  if (!('Notification' in window)) {
    console.log('Navegador não suporta notificações');
    return;
  }
  
  const perm = await Notification.requestPermission();
  if (perm === 'granted') {
    console.log('✅ Permissão concedida!');
    // Mostrar confirmação na página
    window.parent.postMessage({tipo: 'notificacao_ok'}, '*');
  } else if (perm === 'denied') {
    console.log('❌ Permissão negada');
    window.parent.postMessage({tipo: 'notificacao_negada'}, '*');
  }
}

// Pedir automaticamente ao carregar
window.addEventListener('load', pedirPermissao);

// Detectar se pode instalar o app
let eventoInstalar;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  eventoInstalar = e;
  window.parent.postMessage({tipo: 'pode_instalar'}, '*');
});
</script>

<style>
/* Limpar sobras da interface */
[data-testid="stToolbar"], [data-testid="stManageAppMenu"], .stAppHeader { display: none !important; }
.block-container { padding-top: 1rem !important; }
</style>
""", height=0)

# === TÍTULO ===
st.markdown("""
<h1 style='text-align:center;color:#ff0000;margin:0.5rem 0;'>🚨 GECOM SEGURANÇA</h1>
<p style='text-align:center;font-size:1rem;'>Proteção Máxima · Ararica / RS</p>
""", unsafe_allow_html=True)

st.divider()

# === STATUS DAS NOTIFICAÇÕES ===
perm = st.query_params.get("perm", "")

if perm == "ok":
    st.success("✅ Notificações ativadas! Chegarão mesmo com o navegador fechado")
elif perm == "negada":
    st.error("❌ Permissão negada — clique no 🔒 cadeado acima → Permitir notificações")
else:
    st.info("📲 Aguardando permissão... aparecerá uma mensagem → clique em **Permitir** ✅")
    
    if st.button("🔔 Ativar Notificações Agora", type="primary", use_container_width=True):
        st.query_params["perm"] = "pedindo"
        st.rerun()

st.divider()

# === BOTÃO INSTALAR APP ===
st.markdown("### 📲 Instalar na Tela Inicial")
st.info("Instale como aplicativo → abre direto, sem navegador!")

if st.button("➕ Instalar GECOM", use_container_width=True):
    st.toast("📱 No celular: clique nos 3 pontinhos ⋮ → Adicionar à tela inicial ✅")

st.divider()

# === ÚLTIMAS NOTÍCIAS / ALERTAS ===
st.subheader("📢 Últimas Notícias e Alertas")

try:
    resp = requests.get(
        f"{SUPABASE_URL}/alertas?select=*&order=criado_em.desc&limit=10",
        headers={"apikey": CHAVE_SUPABASE},
        timeout=10
    )
    if resp.status_code == 200:
        dados = resp.json()
        if not dados:
            st.info("Nenhuma notificação no momento")
        for alerta in dados:
            st.markdown(f"""
            <div style='border-left:4px solid #ff3333;padding:12px;background:#fff0f0;border-radius:6px;margin:8px 0;'>
            <strong>{alerta.get('titulo', 'Alerta')}</strong><br>
            {alerta.get('mensagem', '')}<br>
            <small style='color:#666'>{alerta.get('criado_em', '')[:19]}</small>
            </div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Não foi possível carregar notícias: {e}")

st.divider()
st.caption("GECOM Segurança · Emergência: 190")
