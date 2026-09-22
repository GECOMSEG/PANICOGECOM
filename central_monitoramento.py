import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="GECOM — Monitoramento", page_icon="🚨", layout="centered")

# === CONFIGURAÇÕES ===
SUPABASE_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1"
CHAVE_SUPABASE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"
VAPID_PUBLICA = "BK...seu-chave-publica-vapid-aqui..."  # Gerar depois

# === REGISTRAR PWA E PUSH ===
st.components.v1.html(f"""
<meta name="theme-color" content="#ff0000">
<link rel="manifest" href="data:application/manifest+json;base64,eyJuYW1lIjoiR0VDT00gU2VndXJhbmNhIiwic2hvcnRfbmFtZSI6IkdFQ09NIiwiZGVzY3JpcHRpb24iOiJQcm90ZcOtc2EgTWF4aW1hIiwiZGVzaWduX3Njb3BlIjoiLyIsInN0YXJ0X3VybCI6Ii8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImJhY2tncm91bmRfY29sb3IiOiIjMGUwMDAwIiwidGhlbWVfY29sb3IiOiNmZjAwMDAiLCJpY29ucyI6W3sic3JjIjoiaHR0cHM6Ly92aWEucGxhY2Vob2xkZXIuY29tLzE5Mi9GRjAwMDAvRkZGRkZGIT90ZXh0PUciLCJzaXplcyI6IjE5MnwxOTIiLCJ0eXBlIjoiaW1hZ2UvcG5nIn1dfQ==">

<script>
if ('serviceWorker' in navigator && 'PushManager' in window) {{
  window.addEventListener('load', async () => {{
    try {{
      const registro = await navigator.serviceWorker.register('/static/sw.js');
      console.log('✅ SW registrado');
      
      // Pedir permissão assim que abrir
      const permissao = await Notification.requestPermission();
      if (permissao === 'granted') {{
        const inscricao = await registro.pushManager.subscribe({{
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array('{VAPID_PUBLICA}')
        }});
        // Enviar inscrição pro teu servidor/Supabase
        await fetch('/_stcore/streamlit', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{tipo: 'inscrever_push', dados: inscricao}})
        }});
      }}
    }} catch (erro) {{
      console.log('⚠️ Push não disponível:', erro);
    }}
  }});
}}

function urlBase64ToUint8Array(base64) {{
  const preenchimento = '='.repeat((4 - base64.length % 4) % 4);
  const base = (base64 + preenchimento).replace(/-/g, '+').replace(/_/g, '/');
  const dados = window.atob(base);
  return Uint8Array.from([...dados].map(c => c.charCodeAt(0)));
}}
</script>

<style>
/* Esconde elementos desnecessários */
header, .stDeployButton, footer {{ display: none !important; }}
</style>
""", height=0)

# === INTERFACE ===
st.markdown("""
<h1 style='text-align:center;color:#ff0000;margin:0'>🚨 GECOM SEGURANÇA</h1>
<p style='text-align:center'>Proteção Máxima · Alertas direto no celular</p>
""", unsafe_allow_html=True)

# Status da notificação
perm = Notification.permission if 'Notification' in dir() else 'default'
if perm == 'granted':
    st.success("✅ Notificações ativadas — chegarão mesmo com o app fechado!")
elif perm == 'denied':
    st.warning("⚠️ Permissão negada — ative nas configurações do navegador")
else:
    st.info("ℹ️ Permita as notificações quando solicitado")

st.divider()

# === ÚLTIMAS NOTÍCIAS / ALERTAS ===
st.subheader("📢 Últimas Notícias e Alertas")

# Buscar do Supabase
try:
    resp = requests.get(f"{SUPABASE_URL}/alertas?select=*&order=criado_em.desc&limit=10",
                        headers={"apikey": CHAVE_SUPABASE})
    if resp.status_code == 200:
        alertas = resp.json()
        if not alertas:
            st.info("Nenhuma notificação no momento")
        for a in alertas:
            st.markdown(f"""
            <div style='border-left:4px solid #ff3333;padding:10px;background:#1a0000;border-radius:4px;margin:8px 0'>
            <strong>{a.get('titulo','Alerta')}</strong><br>
            {a.get('mensagem','')}<br>
            <small style='color:#999'>{a.get('criado_em','')[:19]}</small>
            </div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Erro ao carregar: {e}")
    
