import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# SGI SR. PAPEL - ARCHITECTURE & DESIGN LAYER V2
# DATA ARCHITECT: BRUNA KAMILLE BRITO FERREIRA
# ============================================================

st.set_page_config(page_title="SGI - Sr. Papel", page_icon="📝", layout="wide")

# INTEGRAÇÃO DE DESIGN E ESTILIZAÇÃO VIA INJEÇÃO DE CSS
st.markdown("""
    <style>
        /* Paleta de Cores Corporativa */
        :root {
            --primary: #0F4C81;
            --secondary: #F5F7FA;
            --accent: #D32F2F;
        }
        .main-header {
            background: linear-gradient(135deg, #0F4C81 0%, #1D70B8 100%);
            padding: 30px;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .main-header h1 { color: white !important; font-weight: 800; margin-bottom: 5px; }
        .main-header p { color: #E0F0FF !important; font-size: 16px; margin: 0; }
        
        /* Cards Informativos e UI */
        .product-card {
            background-color: #F8FAFC;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            margin-bottom: 15px;
        }
        .alert-critical {
            background-color: #FFEBEE;
            border-left: 6px solid #D32F2F;
            padding: 15px;
            border-radius: 6px;
            color: #C62828;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 1. PERSISTÊNCIA EM MEMÓRIA (VÍNCULO ESTRITO COM O MER/DICIONÁRIO)
if "produtos_db" not in st.session_state:
    st.session_state.produtos_db = pd.DataFrame([
        {"ID_Produto": 1, "SKU_EAN": "7891011121314", "Nome": "Caneta Stabilo Point 88", "Preco_Varejo": 10.90, "Preco_Atacado": 8.90, "Qtd_Min_Atacado": 12, "Quantidade_Atual": 15, "Ponto_Pedido": 5, "Localizacao": "Corredor A, Prateleira 2"},
        {"ID_Produto": 2, "SKU_EAN": "7892021222324", "Nome": "Caderno Inteligente A5", "Preco_Varejo": 89.90, "Preco_Atacado": 79.90, "Qtd_Min_Atacado": 5, "Quantidade_Atual": 3, "Ponto_Pedido": 5, "Localizacao": "Balcão Central, Gaveta 1"},
        {"ID_Produto": 3, "SKU_EAN": "7893031323334", "Nome": "Bobina Térmica 80x40", "Preco_Varejo": 5.19, "Preco_Atacado": 4.19, "Qtd_Min_Atacado": 30, "Quantidade_Atual": 0, "Ponto_Pedido": 10, "Localizacao": "Depósito Fundo, Palete 3"}
    ])

# 2. CAMADA DE SEGURANÇA E PRIVILÉGIOS (RBAC)
st.sidebar.image("https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=150", width=100) # Ilustração minimalista de papelaria conceitual
st.sidebar.markdown("## 🔐 Controle de Acesso (RBAC)")
perfil = st.sidebar.selectbox(
    "Selecione o perfil de autenticação:",
    ["Cliente (Catálogo Omnichannel)", "Funcionário (Módulo de Caixa - PDV)", "Administrador (Dashboard de BI Gerencial)"]
)

# ------------------------------------------------------------
# PERFIL I: CLIENTE (CATÁLOGO OMNICHANNEL)
# ------------------------------------------------------------
if perfil == "Cliente (Catálogo Omnichannel)":
    st.markdown("""
        <div class='main-header'>
            <h1>SR. PAPEL</h1>
            <p>SGI Centralizado — Solução Omnichannel Integrada</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Hub Unificado de Redirecionamento de Canais (Fim do labirinto As-Is)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("📍 Shopping Center Icaraí (Maps)", "https://maps.google.com")
    with c2:
        st.link_button("💬 Canal Oficial WhatsApp", "https://wa.me/5521999301300")
    with c3:
        st.link_button("👥 Comunidade Papelaria Fofa", "https://chat.whatsapp.com")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📚 Catálogo Interativo de Produtos")
    
    for idx, row in st.session_state.produtos_db.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 3, 2])
            with col1:
                st.markdown(f"### {row['Nome']}")
                st.caption(f"EAN/SKU: {row['SKU_EAN']} | Ponto de Segurança: {row['Ponto_Pedido']} un.")
            with col2:
                st.write(f"**Varejo (B2C):** R$ {row['Preco_Varejo']:.2f}")
                st.write(f"**Atacado (B2B):** R$ {row['Preco_Atacado']:.2f} *(A partir de {row['Qtd_Min_Atacado']} un.)*")
            with col3:
                if row["Quantidade_Atual"] == 0:
                    st.error("❌ Esgotado no Inventário")
                elif row["Quantidade_Atual"] <= row["Ponto_Pedido"]:
                    # Aplicação Crítica da Regra Visual de Escassez (#D32F2F)
                    st.markdown(f"<span style='color:#D32F2F; font-weight:bold;'>🔥 Escassez: Restam apenas {row['Quantidade_Atual']} un!</span>", unsafe_allow_html=True)
                    st.button("Reservar Item", key=f"btn_{row['ID_Produto']}", use_container_width=True)
                else:
                    st.success("✔️ Disponível em Prateleira")
                    st.button("Adicionar", key=f"btn_{row['ID_Produto']}", use_container_width=True)
            st.markdown("---")

# ------------------------------------------------------------
# PERFIL II: FUNCIONÁRIO (MÓDULO DE CAIXA / PDV)
# ------------------------------------------------------------
elif perfil == "Funcionário (Módulo de Caixa - PDV)":
    st.markdown("<div class='main-header'><h1>🏪 INTERFACE DO CAIXA (PDV)</h1><p>Operações de Baixa Carga Cognitiva</p></div>", unsafe_allow_html=True)
    
    sku_input = st.text_input("Bipe o código SKU_EAN do Leitor de Código de Barras:")
    qtd_input = st.number_input("Quantidade de Itens:", min_value=1, value=1)
    
    if st.button("Processar Transação", use_container_width=True):
        prod_match = st.session_state.produtos_db[st.session_state.produtos_db["SKU_EAN"] == sku_input]
        if not prod_match.empty:
            idx = prod_match.index[0]
            if st.session_state.produtos_db.at[idx, "Quantidade_Atual"] >= qtd_input:
                st.session_state.produtos_db.at[idx, "Quantidade_Atual"] -= qtd_input
                st.success("✅ Transação Processada. Abatimento Omnichannel Concluído com Sucesso!")
                st.rerun()
            else:
                st.markdown(f"<div class='alert-critical'>⚠️ Erro de Inventário: Saldo insuficiente. Sistema registra apenas {st.session_state.produtos_db.at[idx, 'Quantidade_Atual']} unidades disponíveis.</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Código EAN não localizado na base relacional.")

# ------------------------------------------------------------
# PERFIL III: ADMINISTRADOR (BI GERENCIAL)
# ------------------------------------------------------------
elif perfil == "Administrador (Dashboard de BI Gerencial)":
    st.markdown("<div class='main-header'><h1>📊 BUSINESS INTELLIGENCE</h1><p>Monitoramento Analítico de Governança</p></div>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("SKUs Monitorados", len(st.session_state.produtos_db))
    with m2:
        st.metric("Rupturas Críticas (Estoque Zerado)", len(st.session_state.produtos_db[st.session_state.produtos_db["Quantidade_Atual"] == 0]))
    with m3:
        st.metric("SLA Google Maps (Meta)", "90%", "+90% de Eficiência")
        
    st.markdown("### 📋 Visão em Tempo Real da Base de Dados (Sincronizada)")
    st.dataframe(st.session_state.produtos_db, use_container_width=True)
