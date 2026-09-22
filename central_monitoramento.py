import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="GECOM — Monitoramento", page_icon="🚨", layout="centered")

# === CONFIGURAÇÕES ===
SUPABASE_URL = "https://hbyqdrewpzjupzyukyts.supabase.co/rest/v1"
CHAVE_SUPABASE = "sb_publishable_t2iYYcgneXOXD9JPW5GcnQ_BisRaVZS"

headers = {
    "apikey": CHAVE_SUPABASE,
    "Authorization": f"Bearer {CHAVE_SUPABASE}",
    "Content-Type": "application/json"
}

# === INTERFACE ===
st.markdown("""
<style>
[data-testid="stToolbar"], .stAppHeader { display: none !important; }
.block-container { padding-top: 1rem !important; }
</style>
<h1 style='text-align:center;color:#ff0000;margin:0.3rem 0;'>🚨 GECOM SEGURANÇA</h1>
<p style='text-align:center;'>Proteção Máxima · Ararica / RS</p>
""", unsafe_allow_html=True)

st.divider()
st.success("✅ Conectado! Buscando eventos...")
st.divider()

# === BUSCAR ALERTAS — NOMES EXATOS DAS COLUNAS ===
st.subheader("📢 Últimos Eventos")

with st.spinner("Carregando..."):
    try:
        # Ordenando por hora decrescente (mais recente primeiro)
        resp = requests.get(
            f"{SUPABASE_URL}/alertas?select=*&order=hora.desc&limit=10",
            headers=headers,
            timeout=15
        )

        if resp.status_code == 200:
            dados = resp.json()
            
            if not dados:
                st.info("ℹ️ Nenhum evento registrado ainda.")
                st.info("Clique abaixo para criar o primeiro:")
                
                if st.button("📝 Criar evento de teste", type="primary", use_container_width=True):
                    novo = {
                        "nome": "Teste GECOM",
                        "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "endereço": "Ararica / RS — Teste",
                        "lat": "",
                        "lon": "",
                        "obs": "Sistema funcionando perfeitamente! ✅",
                        "mapa": ""
                    }
                    resp_post = requests.post(f"{SUPABASE_URL}/alertas", json=novo, headers=headers)
                    if resp_post.status_code in [200, 201]:
                        st.success("✅ Criado com sucesso! Atualize a página 🔄")
                        st.rerun()
                    else:
                        st.error(f"❌ Erro ao salvar: {resp_post.status_code}")
            else:
                st.success(f"✅ {len(dados)} evento(s) encontrado(s)!")
                
                for evt in dados:
                    # Link do mapa se tem lat/lon
                    link_mapa = ""
                    if evt.get("lat") and evt.get("lon"):
                        link_mapa = f"🔗 <a href='https://www.google.com/maps/search/?api=1&query={evt['lat']},{evt['lon']}' target='_blank'>Ver no Mapa</a>"
                    elif evt.get("mapa"):
                        link_mapa = f"🔗 <a href='{evt['mapa']}' target='_blank'>Ver no Mapa</a>"
                    
                    st.markdown(f"""
                    <div style='border-left:4px solid #ff3333;padding:12px;background:#fff0f0;border-radius:6px;margin:8px 0;'>
                    <strong>{evt.get('nome', 'Alerta')}</strong><br>
                    🕒 {evt.get('hora', 'Sem data')}<br>
                    📍 {evt.get('endereço', 'Sem endereço')}<br>
                    📝 {evt.get('obs', 'Sem descrição')}<br>
                    {link_mapa}
                    </div>
                    """, unsafe_allow_html=True)
                    
        elif resp.status_code == 404:
            st.error("❌ Tabela 'alertas' não encontrada")
        else:
            st.error(f"Erro: {resp.status_code}")

    except Exception as e:
        st.error(f"⚠️ Erro: {str(e)}")

st.divider()
st.caption("GECOM Segurança · Emergência: 190")
