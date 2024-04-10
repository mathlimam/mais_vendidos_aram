import pandas as pd
import plotly.express as px
import streamlit as st

dataframe = pd.read_excel("database.xlsx")



def faturamento_por_grupo(sdf):
    # Gráfico de barras para o faturamento total por grupo
    new_df = sdf.sort_values("FATURAMENTO TOTAL")
    #fig = px.bar(new_df.groupby('GRUPO')['FATURAMENTO TOTAL'].sum().reset_index(), x='GRUPO', y="FATURAMENTO TOTAL", title="Faturamento total por grupo")
    #st.plotly_chart(fig)

    fig = px.bar(new_df.groupby('GRUPO')['FATURAMENTO TOTAL'].sum().reset_index(), 
             x='GRUPO', 
             y="FATURAMENTO TOTAL", 
             title="Faturamento total por grupo", 
             category_orders={'GRUPO': new_df.groupby('GRUPO')['FATURAMENTO TOTAL'].sum().sort_values(ascending=False).index.tolist()})
    st.plotly_chart(fig)

def produtos_mais_vendidos_por_grupo(sdf, grupo_selecionado):
    # Filtrar por grupo selecionado
    produtos_grupo_selecionados = sdf[sdf['GRUPO'] == grupo_selecionado]
    produtos_grupo_selecionados = produtos_grupo_selecionados.sort_values("QUANTIDADE_x", ascending=False)

    # Gráfico de barras verticais para os produtos mais vendidos no grupo selecionado
    fig = px.bar(
        produtos_grupo_selecionados,
        x='PRODUTO',
        y='QUANTIDADE_x',
        title=f"Produtos mais vendidos no grupo {grupo_selecionado}",
        labels={'QUANTIDADE_x': 'Quantidade', 'PRODUTO': 'Produto'},
        color='QUANTIDADE_x',  # Adicionando escala de cores
        color_continuous_scale='Viridis',  # Escolhendo um mapa de cores (pode ser ajustado)

    )

    # Configurar layout para largura de 100%
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=50))  # Ajuste a largura conforme necessário

    st.write(f"Produtos do grupo {grupo_selecionado}:")
    st.plotly_chart(fig, use_container_width=True)


def produtos_mais_vendidos(sdf):
    new_df  =sdf.sort_values("QUANTIDADE_x", ascending=False).head(13)
    new_df = new_df[new_df["LINHA"] != "EQUIPAMENTOS E ACESSORIOS"]
    new_df = new_df[new_df["LINHA"] != "MATERIAL CONSUMO"]
    new_df = new_df[new_df["LINHA"] != ""]
    fig = px.bar(new_df,
                 x="PRODUTO",
                 y="QUANTIDADE_x",
                 title="Os 10 produtos mais vendidos (Quantidade)", 
                 labels={"QUANTIDADE": "Quantidade",  "PRODUTO":"Produto"},
                 color="QUANTIDADE_x")
    st.plotly_chart(fig)

def produtos_menos_lucrativos(sdf):
    new_df  =sdf.sort_values("LUCRO", ascending=True).head(30)
    new_df = new_df[new_df["LINHA"] != "EQUIPAMENTOS E ACESSORIOS"]
    new_df = new_df[new_df["LINHA"] != "MATERIAL CONSUMO"]
    new_df = new_df[new_df["GRUPO"] != "SAZONAL"]
    fig = px.bar(new_df,
                 x="PRODUTO",
                 y="LUCRO",
                 title="Os 20 produtos menos lucrativos", 
                 labels={"LUCRO": "Lucro Bruto",  "PRODUTO":"Produto"},
                 color="LUCRO")
    st.plotly_chart(fig, use_container_width=True)

def produtos_mais_lucrativos(sdf):

    new_df  =sdf.sort_values("LUCRO", ascending=False).head(20)
    new_df = new_df[new_df["LINHA"] != "EQUIPAMENTOS E ACESSORIOS"]
    new_df = new_df[new_df["LINHA"] != "MATERIAL CONSUMO"]
    new_df = new_df[new_df["GRUPO"] != "SAZONAL"]

    fig = px.bar(new_df,
                 x="PRODUTO",
                 y="LUCRO",
                 title="Os 20 produtos mais lucrativos ", 
                 labels={"LUCRO": "Lucro Bruto",  "PRODUTO":"Produto"},
                 color="LUCRO",
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    

def main():
    # Leitura do arquivo Excel
    sdf = pd.read_excel("sales_db.xlsx")
    st.set_page_config(layout='wide')

    # Escolher entre análise de produtos e clientes
    
    st.title('Análise de dados')

    # Layout com duas colunas
    left, right = st.columns(2)

    # Executar a análise de produtos

    with left:
            faturamento_por_grupo(sdf)
            
    with right:
            produtos_mais_vendidos(sdf)

    
        # Seleção do grupo
    grupo_selecionado = st.selectbox("Selecione um grupo", sdf['GRUPO'].unique())

        # Lógica para mostrar os produtos mais vendidos no grupo selecionado
    if grupo_selecionado:
            produtos_mais_vendidos_por_grupo(sdf, grupo_selecionado)

    produtos_mais_lucrativos(sdf)
    produtos_menos_lucrativos(sdf)

    # Adicionar aqui a lógica para a análise de clientes se necessário

if __name__ == '__main__':
   
    main()
