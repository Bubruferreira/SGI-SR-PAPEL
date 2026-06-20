import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# SGI SR. PAPEL - INTERFACE OMNICHANNEL UNIFICADA
# REQUISITOS DE DESIGN, LOGIC UI, RBAC E ENGENHARIA DE DADOS
# AUTORA: BRUNA KAMILLE BRITO FERREIRA (DATA ARCHITECT)
# ============================================================

st.set_page_config(page_title="SGI - Sr. Papel", page_icon="📝", layout="wide")

# 1. PERSISTÊNCIA EM MEMÓRIA (REPLICANDO ESTRUTURA DO MER E CARGA INICIAL DO CHECKLIST 1)
if "produtos_db" not in st.session_state:
    st.session_state.produtos_db = pd.DataFrame([
        {"ID_Produto": 1, "SKU_EAN": "7891011121314", "Nome": "Caneta Stabilo Point 88", "Preco_Varejo": 10.90, "Preco_Atacado": 8.90, "Qtd_Min_Atacado": 12, "Quantidade_Atual": 15, "Ponto_Pedido": 5, "Localizacao": "Corredor A, Prateleira 2"},
        {"ID_Produto": 2, "SKU_EAN": "7892021222324", "Nome": "Caderno Inteligente A5", "Preco_Varejo": 89.90, "Preco_Atacado": 79.90, "Qtd_Min_Atacado": 5, "Quantidade_Atual": 3, "Ponto_Pedido": 5, "Localizacao": "Balcão Central, Gaveta 1"},
        {"ID_Produto": 3, "SKU_EAN": "7893031323334", "Nome": "Bobina Térmica 80x40", "Preco_Varejo": 5.19, "Preco_Atacado": 4.19, "Qtd_Min_Atacado": 30, "Quantidade_Atual": 0, "Ponto_Pedido": 10, "Localizacao": "Depósito Fundo, Palete 3"}
    ])

if "vendas_historico" not in st.session_state:
    st.session_state.vendas_historico = []

# ESTILIZAÇÃO DO TÍTULO E CORES DA MARCA
st.markdown("""
    <style>
        .main-title { font-size:36px; font-weight:bold; color:#0F4C81; text-align:center; margin-bottom:20px; }
        .card-critico { background-color: #FFEBEE; border-left: 5px solid #D32F2F; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. CONTROLE DE ACESSO BASEADO EM PAPÉIS (RBAC) - EXIGÊNCIA DO PROJETO
st.sidebar.markdown("## 🔐 Controle de Acesso (RBAC)")
perfil = st.sidebar.selectbox(
    "Selecione o perfil de acesso para simulação:",
    ["Cliente (Catálogo Web - B2C/B2B)", "Funcionário (Módulo de Caixa - PDV)", "Administrador (Dashboard de BI Gerencial)"]
)

# ------------------------------------------------------------
# PERFIL I: CLIENTE (CATÁLOGO WEB OMNICHANNEL) - RF01, RF02, RF04, RF07
# ------------------------------------------------------------
if perfil == "Cliente (Catálogo Web - B2C/B2B)":
    st.markdown("<div class='main-title'>🛍️ Catálogo Digital Interativo — Sr. Papel</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Redirecionamento Inteligente e Hub de Informações (RF01, RF04)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("📍 Localização (Google Maps)", "https://maps.google.com")
    with c2:
        st.link_button("💬 WhatsApp Oficial (Varejo)", "https://wa.me/5521999301300")
    with c3:
        st.link_button("👥 Grupo Papelaria Fofa (Novidades)", "https://chat.whatsapp.com")
        
    st.markdown("---")
    
    # Renderização Dinâmica dos Itens (Substituindo o PDF estático)
    for idx, row in st.session_state.produtos_db.iterrows():
        col1, col2, col3 = st.columns([3, 3, 2])
        
        with col1:
            st.markdown(f"### {row['Nome']}")
            st.caption(f"Código EAN/SKU: {row['SKU_EAN']}")
            
        with col2:
            st.write(f"**Preço Varejo (B2C):** R$ {row['Preco_Varejo']:.2f}")
            st.write(f"**Preço Atacado (B2B):** R$ {row['Preco_Atacado']:.2f} *(Gatilho: a partir de {row['Qtd_Min_Atacado']} unidades)*")
            
        with col3:
            # REGRAS DE COMPORTAMENTO DE INTERFACE (LOGIC UI) E ADERÊNCIA AO CHECKLIST 2
            if row["Quantidade_Atual"] == 0:
                st.error("❌ Produto Temporariamente Esgotado")
                st.button("Avise-me quando chegar", key=f"avise_{row['ID_Produto']}")
            elif row["Quantidade_Atual"] <= row["Ponto_Pedido"]:
                # Alerta Crítico de Escassez - Vermelho Vibrante (#D32F2F)
                st.markdown(f"<span style='color:#D32F2F; font-weight:bold; font-size:16px;'>🔥 Corra! Restam apenas {row['Quantidade_Atual']} unidades em estoque!</span>", unsafe_allow_html=True)
                st.button("Adicionar ao Carrinho", key=f"buy_{row['ID_Produto']}")
            else:
                st.success("✔️ Item Disponível em Prateleira")
                st.button("Adicionar ao Carrinho", key=f"buy_{row['ID_Produto']}")
        st.markdown("---")

# ------------------------------------------------------------
# PERFIL II: FUNCIONÁRIO (MÓDULO DE CAIXA / PDV MINIMALISTA) - RF03, RF06
# ------------------------------------------------------------
elif perfil == "Funcionário (Módulo de Caixa - PDV)":
    st.markdown("<div class='main-title'>🏪 Ponto de Venda (PDV) — Módulo de Caixa</div>", unsafe_allow_html=True)
    st.markdown("### Interface de Baixa Carga Cognitiva para Operação")
    
    # Simulação de botões grandes para o "Modo Tio" (Checklist 2)
    st.markdown("#### ⚡ Atalhos Rápidos (Modo Simplificado)")
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        if st.button("📝 Baixa: 1 Caneta Stabilo", use_container_width=True):
            st.session_state.produtos_db.at[0, "Quantidade_Atual"] -= 1
            st.success("Abatimento automático realizado via atalho.")
            st.rerun()
            
    with b_col2:
        if st.button("📘 Baixa: 1 Caderno Inteligente", use_container_width=True):
            if st.session_state.produtos_db.at[1, "Quantidade_Atual"] > 0:
                st.session_state.produtos_db.at[1, "Quantidade_Atual"] -= 1
                st.success("Abatimento automático realizado via atalho.")
                st.rerun()
            else:
                st.error("Erro: Estoque zerado.")
                
    st.markdown("---")
    
    # Entrada Manual via Código de Barras (Leitor Ótico)
    sku_input = st.text_input("Bipe o Código de Barras do Produto (SKU_EAN):")
    qtd_input = st.number_input("Quantidade de Itens da Venda:", min_value=1, value=1, step=1)
    
    if st.button("Confirmar Venda e Registrar Saída Omnichannel"):
        prod_match = st.session_state.produtos_db[st.session_state.produtos_db["SKU_EAN"] == sku_input]
        
        if not prod_match.empty:
            idx = prod_match.index[0]
            saldo_disponivel = st.session_state.produtos_db.at[idx, "Quantidade_Atual"]
            
            if saldo_disponivel >= qtd_input:
                # Gatilho de Sincronização Omnichannel (RF06, Trigger de Abatimento)
                st.session_state.produtos_db.at[idx, "Quantidade_Atual"] -= qtd_input
                st.balloons()
                st.success(f"✅ Transação concluída! {qtd_input} unidade(s) de '{st.session_state.produtos_db.at[idx, 'Nome']}' abatida(s) do estoque digital instantaneamente.")
                st.rerun()
            else:
                # Alerta de Auditoria e Segurança de Inventário
                st.markdown(f"<div class='card-critico'><strong>⚠️ Alerta de Segurança:</strong> Tentativa de venda de item com estoque insuficiente. Saldo em sistema: {saldo_disponivel} unidades. Deseja forçar auditoria física?</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Código EAN não localizado no banco de dados. Cadastre o produto antes de operar.")

# ------------------------------------------------------------
# PERFIL III: ADMINISTRADOR (DASHBOARD DE BI GERENCIAL) - RF05, RF08, RN06
# ------------------------------------------------------------
elif perfil == "Administrador (Dashboard de BI Gerencial)":
    st.markdown("<div class='main-title'>📊 Business Intelligence — Painel Administrativo</div>", unsafe_allow_html=True)
    st.markdown("### Monitoramento Estratégico e Saúde Digital")
    
    # Cálculo de Métricas e KPIs de Negócio
    total_produtos = len(st.session_state.produtos_db)
    itens_esgotados = len(st.session_state.produtos_db[st.session_state.produtos_db["Quantidade_Atual"] == 0])
    itens_criticos = len(st.session_state.produtos_db[(st.session_state.produtos_db["Quantidade_Atual"] > 0) & (st.session_state.produtos_db["Quantidade_Atual"] <= st.session_state.produtos_db["Ponto_Pedido"])])
    
    # Exibição de Cards de Indicadores (Métricas de Sucesso)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total de SKUs Cadastrados", total_produtos)
    with m2:
        st.metric("Produtos Esgotados (Ruptura)", itens_esgotados)
    with m3:
        st.metric("Alertas de Reposição Crítica", itens_criticos)
    with m4:
        st.metric("SLA de Resposta Google Maps (Meta)", "90%", "+90% de ganho")
        
    st.markdown("---")
    
    # Tabela Completa Baseada na Visão Exclusiva do Administrador (RN06)
    st.markdown("### 📋 Visão Holística do Inventário (Dados Vinculados ao MER)")
    st.dataframe(st.session_state.produtos_db, use_container_width=True)
    
    # Simulação da Automação da Lista de Compras Semanais
    st.markdown("### 🛒 Sugestão de Reposição Automatizada (Alerta de Comportamento)")
    produtos_alerta = st.session_state.produtos_db[st.session_state.produtos_db["Quantidade_Atual"] <= st.session_state.produtos_db["Ponto_Pedido"]]
    
    if not produtos_alerta.empty:
        for _, prod in produtos_alerta.iterrows():
            st.warning(f"⚠️ **Item Requisitado:** {prod['Nome']} | **Saldo Atual:** {prod['Quantidade_Atual']} un. | **Localização:** {prod['Localizacao']}")
    else:
        st.success("✅ Estoque operando acima das margens críticas de segurança. Nenhuma ação recomendada.")
