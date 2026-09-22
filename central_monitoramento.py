import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="GECOM — Monitoramento", page_icon="🚨", layout="centered")

# === CONFIGURAÇÕES ===
SUPABASE_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1"
CHAVE_SUPABASE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"

# Chave VAPID — para notificações Push (já configurada)
VAPID_PUBLICA = "BC8RzZ_TwYb6KZvFz8xX7Y9z9X7b6KZvFz8xX7Y9z9X7b6KZvFz8xX7Y9z9X7b6KZvFz8xX7Y9z9X7b6KZvFz8xX7Y9z9X7b6KZvFz8xX7Y"

headers = {
    "apikey": CHAVE_SUPABASE,
    "Authorization": f"Bearer {CHAVE_SUPABASE}",
    "Content-Type": "application/json"
}

# === PWA + PUSH — NOTIFICAÇÃO FECHADO ===
st.components.v1.html(f"""
<meta name="theme-color" content="#ff0000">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

<link rel="manifest" href="data:application/manifest+json;base64,eyJuYW1lIjoiR0VDT00gU2VndXJhbmNhIiwic2hvcnRfbmFtZSI6IkdFQ09NIiwiZGVzY3JpcHRpb24iOiJQcm90ZcOtc2EgTWF4aW1hIiwiZGVzaWduX3Njb3BlIjoiLyIsInN0YXJ0X3VybCI6Ii8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImJhY2tncm91bmRfY29sb3IiOiIjMGUwMDAwIiwidGhlbWVfY29sb3IiOiNmZjAwMDAiLCJpY29ucyI6W3sic3JjIjoiaHR0cHM6Ly92aWEucGxhY2Vob2xkZXIuY29tLzE5Mi9GRjAwMDAvRkZGRkZGIT90ZXh0PUciLCJzaXplcyI6IjE5MnwxOTIiLCJ0eXBlIjoiaW1hZ2UvcG5nIn1dfQ==">

<script>
let inscricaoPush = null;

function urlBase64ToUint8Array(base64) {{
  const preenchimento = '='.repeat((4 - base64.length % 4) % 4);
  const base = (base64 + preenchimento).replace(/-/g, '+').replace(/_/g, '/');
  const dados = window.atob(base);
  return Uint8Array.from([...dados].map(c => c.charCodeAt(0)));
}}

async function ativarPush() {{
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {{
    console.log('Push não suportado');
    return;
  }}

  try {{
    const registro = await navigator.serviceWorker.register('/sw.js');
    inscricaoPush = await registro.pushManager.subscribe({{
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array('{VAPID_PUBLICA}')
    }});
    console.log('✅ Push ativado!');
    // Salvar inscrição no Supabase
    await fetch('/_stcore/streamlit', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{push: inscricaoPush}})
    }});
  }} catch (erro) {{
    console.log('⚠️ Push não ativado:', erro);
  }}
}}

// Pedir permissão e ativar push ao carregar
window.addEventListener('load', async () => {{
  if (Notification.permission === 'default') {{
    const perm = await Notification.requestPermission();
    if (perm === 'granted') ativarPush();
  }} else if (Notification.permission === 'granted') {{
    ativarPush();
  }}
}});
</script>

<style>
[data-testid="stToolbar"], .stAppHeader {{ display: none !important; }}
.block-container {{ padding-top: 1rem !important; }}
</style>
""", height=0)

# === TÍTULO ===
st.markdown("""
<h1 style='text-align:center;color:#ff0000;margin:0
10rem 0;'>🚨GECOM SEGURANÇA</h1>
<p style='text-align:center;'>PROTEÇÃO MÁXIMA ✅</p>
""", unsafe_allow_html=True)

st.divider()

# === STATUS PUSH ===
perm = st.query_params.get("perm", "")
if perm == "ok":
    st.success("✅ Push ATIVADO! Notificações chegam com tudo fechado!")
elif perm == "negada":
    st.error("❌ Permissão negada → 🔒 Cadeado → Permitir notificações")
else:
    st.info("🔔 Permita as notificações quando solicitado — é só uma vez!")

st.divider()

# === ÚLTIMOS EVENTOS ===
st.subheader("📢EVENTOS RECEBIDOS")

with st.spinner("Carregando..."):
    try:
        resp = requests.get(
            f"{SUPABASE_URL}/alertas?select=*&order=hora.desc&limit=10",
            headers=headers,
            timeout=15
        )

        if resp.status_code == 200:
            dados = resp.json()
            
            if not dados:
                st.info("ℹ️ Nenhum evento registrado.")
            else:
                st.success(f"✅ {len(dados)} evento(s) encontrado(s)!")
                
                for evt in dados:
                    link_mapa = ""
                    if evt.get("lat") and evt.get("lon"):
                        link_mapa = f"🔗 <a href='https://www.google.com/maps/search/?api=1&query={evt['lat']},{evt['lon']}' target='_blank'>Ver no Mapa</a>"
                    elif evt.get("mapa"):
                        link_mapa = f"🔗 <a href='{evt['mapa']}' target='_blank'>Ver no Mapa</a>"
                    
                    endereco_exibicao = evt.get("endereço") or "Sem endereço"
                    if not evt.get("endereço") and evt.get("lat") and evt.get("lon"):
                        endereco_exibicao = f"📍 {evt['lat']}, {evt['lon']}"
                    
                    st.markdown(f"""
                    <div style='border-left:4px solid #ff3333;padding:12px;background:#fff0f0;border-radius:6px;margin:8px 0;'>
                    <strong>{evt.get('nome', 'Alerta')}</strong><br>
                    🕒 {evt.get('hora', 'Sem data')}<br>
                    📍 {endereco_exibicao}<br>
                    📝 {evt.get('obs', 'Sem descrição')}<br>
                    {link_mapa}
                    </div>
                    """, unsafe_allow_html=True)
                    
    except Exception as e:
        st.warning(f"Conectando... {str(e)}")

st.divider()
st.caption("GECOM Segurança · Notificações Push Ativadas · Emergência: 190")
