import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def carregaDados(caminho):
    dados = pd.read_csv(caminho)

    return dados


def graficoComparativo(dadosUm, dadosDois, causa = "Todas", estado = "Brasil"):
    if (estado == "Brasil") * (causa == "Todas"):
        totalUm = dadosUm["total"].sum()
        totalDois = dadosDois["total"].sum()
        lista = [int(totalUm), int(totalDois)]
        causa = "todas as causas"
        estado = "todos os estados do Brasil"

    elif estado == "Brasil":
        totalUm = dadosUm.groupby(["tipo_doenca"]).sum()
        totalDois = dadosDois.groupby(["tipo_doenca"]).sum()
        lista = [int(totalUm.loc[causa]), int(totalDois.loc[causa])]
        estado = "todos os estados do Brasil"

    elif causa == "Todas":
        totalUm = dadosUm.groupby(["uf"]).sum()
        totalDois = dadosDois.groupby(["uf"]).sum()
        lista = [int(totalUm.loc[estado]), int(totalDois.loc[estado])]
        causa = "todas as causas"

    else:
        totalUm = dadosUm.groupby(["tipo_doenca", "uf"]).sum()
        totalDois = dadosDois.groupby(["tipo_doenca", "uf"]).sum()
        lista = [int(totalUm.loc[causa, estado]), int(totalDois.loc[causa, estado])]

    dados = pd.DataFrame({"Total": lista, "Ano": [2019, 2020]})

    
    fig, ax = plt.subplots()
    ax = sns.barplot(x = "Ano", y = "Total", data = dados)
    fig.set_size_inches(8, 5) 
    ax.set_title(f"Óbitos por {causa}, em {estado}")
    #plt.show()

    return dados, fig


def main():
    dados2019 = carregaDados("dados/obitos-2019.csv")
    dados2020 = carregaDados("dados/obitos-2020.csv")
    
    st.title("Análise de óbitos 2019-2020")
    st.markdown("Este trabalho analisa os dados de óbitos por diversas causas nos anos de 2019 e 2020")

    #st.dataframe(dados2019)
    #st.text("Teste")
    #"Teste"
    
    selecionarEstado = np.append(dados2019["uf"].unique(), "Brasil")
    selecionarDoenca = np.append(dados2019["tipo_doenca"].unique(), "Todas")

    estadoSelecionado = st.sidebar.selectbox("Selecione o estado:", selecionarEstado, index = len(selecionarEstado)-1)
    doencaSelecionada = st.sidebar.selectbox("Selecione a doença:", selecionarDoenca, index = len(selecionarDoenca)-1)

    dados, grafico = graficoComparativo(dados2019, dados2020, causa = doencaSelecionada, estado = estadoSelecionado)
    st.pyplot(grafico)
    
    with st.beta_expander("Veja os dados plotados", expanded=False):
        st.dataframe(dados)


if __name__ == "__main__":
    main()
