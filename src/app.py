import streamlit as st
import pandas as pd

# ============================================================
# SGI SR. PAPEL - OMNICHANNEL WEB APP (UI/UX OTIMIZADA)
# ============================================================

st.set_page_config(page_title="Sr. Papel | Hub Web", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

# 1. INJEÇÃO DE CSS AVANÇADO (Design mais limpo e moderno)
st.markdown("""
    <style>
        .title-box {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .title-box h1 { color: white !important; font-weight: 800; font-size: 2.8rem; margin: 0; padding: 0; }
        .title-box p { color: #E0F2FE !important; font-size: 1.2rem; margin-top: 5px; }
        .escassez { color: #D32F2F; font-weight: 800; font-size: 1.1rem; }
        .esgotado { color: #9E9E9E; text-decoration: line-through; }
        .metric-card { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# 2. BANCO DE DADOS EM MEMÓRIA (Simulando a Nuvem)
if "produtos_db" not in st.session_state:
    st.session_state.produtos_db = pd.DataFrame([
        {"ID_Produto": 1, "SKU_EAN": "789101", "Nome": "Caneta Stabilo Boss", "Preco_Varejo": 10.90, "Preco_Atacado": 8.90, "Qtd_Min_Atacado": 12, "Quantidade_Atual": 15, "Ponto_Pedido": 5},
        {"ID_Produto": 2, "SKU_EAN": "789202", "Nome": "Caderno Inteligente", "Preco_Varejo": 89.90, "Preco_Atacado": 79.90, "Qtd_Min_Atacado": 5, "Quantidade_Atual": 3, "Ponto_Pedido": 5},
        {"ID_Produto": 3, "SKU_EAN": "789303", "Nome": "Bobina Térmica", "Preco_Varejo": 5.19, "Preco_Atacado": 4.19, "Qtd_Min_Atacado": 30, "Quantidade_Atual": 0, "Ponto_Pedido": 10},
        {"ID_Produto": 4, "SKU_EAN": "789404", "Nome": "Post-it Amarelo", "Preco_Varejo": 8.50, "Preco_Atacado": 6.50, "Qtd_Min_Atacado": 10, "Quantidade_Atual": 20, "Ponto_Pedido": 8}
    ])

# 3. MENU LATERAL (RBAC - Role-Based Access Control)
st.sidebar.markdown("## 🔐 Controle de Acesso")
perfil = st.sidebar.radio(
    "Selecione a Visão:",
    ["🛒 Cliente (Catálogo Web)", "🏪 Caixa (Funcionária)", "📊 Painel BI (Gerência)"]
)

# ============================================================
# TELA 1: CLIENTE (Layout em Grade estilo E-commerce)
# ============================================================
if perfil == "🛒 Cliente (Catálogo Web)":
    st.markdown("<div class='title-box'><h1>Sr. Papel</h1><p>Catálogo Oficial • Atualizado em Tempo Real</p></div>", unsafe_allow_html=True)
    
    # Botões de Roteamento (Hub Central)
    c1, c2, c3 = st.columns(3)
    c1.link_button("📍 Como Chegar (Icaraí)", "https://maps.google.com", use_container_width=True)
    c2.link_button("💬 Falar no WhatsApp Oficial", "https://wa.me/5521999301300", use_container_width=True)
    c3.link_button("✨ Grupo Papelaria Fofa", "https://chat.whatsapp.com", use_container_width=True)
    
    st.divider()
    st.subheader("🛍️ Vitrine de Produtos")
    
    # Criando um layout de Grid (Grade) real
    cols = st.columns(3)
    for idx, row in st.session_state.produtos_db.iterrows():
        with cols[idx % 3]:
            with st.container(border=True): # Borda nativa bonita do Streamlit
                st.markdown(f"### {row['Nome']}")
                st.caption(f"Código: {row['SKU_EAN']}")
                
                st.write(f"**Varejo:** R$ {row['Preco_Varejo']:.2f}")
                st.write(f"**Atacado:** R$ {row['Preco_Atacado']:.2f} *(a partir de {row['Qtd_Min_Atacado']} un)*")
                
                # Regras de Negócio e Cores de UI (Escassez e Esgotado)
                if row["Quantidade_Atual"] == 0:
                    st.markdown("<p class='esgotado'>❌ Esgotado</p>", unsafe_allow_html=True)
                    st.button("Avise-me quando chegar", key=f"btn_{row['ID_Produto']}", use_container_width=True, disabled=True)
                elif row["Quantidade_Atual"] <= row["Ponto_Pedido"]:
                    st.markdown(f"<p class='escassez'>🔥 Restam só {row['Quantidade_Atual']} unidades!</p>", unsafe_allow_html=True)
                    st.button("Comprar Agora", key=f"btn_{row['ID_Produto']}", type="primary", use_container_width=True)
                else:
                    st.markdown("<p style='color: #2E7D32; font-weight: bold;'>✔ Em Estoque</p>", unsafe_allow_html=True)
                    st.button("Comprar", key=f"btn_{row['ID_Produto']}", use_container_width=True)

# ============================================================
# TELA 2: CAIXA / PDV (Layout Minimalista "Modo Tio")
# ============================================================
elif perfil == "🏪 Caixa (Funcionária)":
    st.markdown("<div class='title-box'><h1>🏪 PDV Rápido</h1><p>Registro de Saída de Estoque</p></div>", unsafe_allow_html=True)
    
    # Fast POS / Botões de Venda Rápida
    st.subheader("⚡ Botões de Venda Rápida")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🖋️ Vender 1x Caneta Stabilo", use_container_width=True):
        st.session_state.produtos_db.loc[0, "Quantidade_Atual"] -= 1
        st.success("Caneta Stabilo vendida! Estoque atualizado na nuvem.")
    if col2.button("📒 Vender 1x Caderno", use_container_width=True):
        st.session_state.produtos_db.loc[1, "Quantidade_Atual"] -= 1
        st.success("Caderno vendido! Estoque atualizado na nuvem.")
        
    st.divider()
    
    # Leitor de Código de Barras
    st.subheader("🔎 Busca por Leitor (Bipar)")
    c1, c2 = st.columns([3, 4])
    with c1:
        sku_input = st.text_input("Código SKU/EAN:", placeholder="Ex: 789101", label_visibility="collapsed")
    with c2:
        if st.button("Confirmar Baixa", type="primary", use_container_width=True):
            idx = st.session_state.produtos_db.index[st.session_state.produtos_db["SKU_EAN"] == sku_input].tolist()
            if idx:
                if st.session_state.produtos_db.at[idx, "Quantidade_Atual"] > 0:
                    st.session_state.produtos_db.at[idx, "Quantidade_Atual"] -= 1
                    st.success("✅ Produto abatido do estoque com sucesso!")
                else:
                    st.error("❌ Atenção: Produto já consta como ZERADO no sistema.")
            else:
                st.warning("⚠️ Código não encontrado.")

# ============================================================
# TELA 3: ADMINISTRADOR / BI (Dashboard Visual)
# ============================================================
elif perfil == "📊 Painel BI (Gerência)":
    st.markdown("<div class='title-box'><h1>📊 Dashboard BI</h1><p>Inteligência de Negócio Sr. Papel</p></div>", unsafe_allow_html=True)
    
    # Cards de KPI
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📦 SKUs Ativos", len(st.session_state.produtos_db))
    m2.metric("🚨 Produtos Esgotados", len(st.session_state.produtos_db[st.session_state.produtos_db["Quantidade_Atual"] == 0]))
    m3.metric("📱 Cliques no WhatsApp", "142", "+12% hoje")
    m4.metric("⭐ SLA de Respostas", "100%", "Sem atrasos")
    
    st.divider()
    
    # Gráfico Visual (Bem melhor que apenas tabela)
    st.subheader("📉 Nível de Estoque Atual (Curva de Escassez)")
    chart_data = st.session_state.produtos_db[["Nome", "Quantidade_Atual"]].set_index("Nome")
    st.bar_chart(chart_data, color="#3B82F6")
    
    # Tabela Gerencial (Com cores)
    st.subheader("📋 Tabela Gerencial de Produtos")
    st.dataframe(
        st.session_state.produtos_db,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Preco_Varejo": st.column_config.NumberColumn("Varejo (R$)", format="R$ %.2f"),
            "Preco_Atacado": st.column_config.NumberColumn("Atacado (R$)", format="R$ %.2f")
        }
    )
