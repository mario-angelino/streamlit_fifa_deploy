import streamlit as st
import pandas as pd
import webbrowser as wb
from datetime import datetime

st.set_page_config(
    page_title='Home',
    page_icon='🏠',
    layout='wide'
)

if "data" not in st.session_state:
    df_data = pd.read_csv('datasets/CLEAN_FIFA23_official_data.csv', index_col=0)
    df_data = df_data[df_data['Contract Valid Until'] >= datetime.today().year]
    df_data = df_data[df_data['Value(£)'] > 0]
    df_data = df_data.sort_values(by='Overall', ascending=False)
    st.session_state["data"] = df_data

st.markdown('# FIFA23 OFFICIAL DATASET! ⚽')
st.sidebar.markdown('Desenvolvido por [Mario Angelino](http://agentlabs.com.br)')

#btn = st.button('Acesse os dados no Kaggle')
#if btn:
#    wb.open_new_tab('https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data')

btn = st.link_button(
    'Acesse os dados no Kaggle',
    'https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data'
    )

st.markdown(
    """
    <div style='text-align: justify;'><p></p>
        <p>The Football Player Dataset from 2017 to 2023 provides comprehensive information about professional football players. 
        The dataset contains a wide range of attributes, including player demographics, physical characteristics, playing statistics, 
        contract details, and club affiliations.</p>
        <p><b>With over 17,000 records</b>, this dataset offers a valuable resource for football analysts, 
        researchers, and enthusiasts interested in exploring various aspects of the footballing world, as it allows for studying player 
        attributes, performance metrics, market valuation, club analysis, player positioning, and player development over time.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: justify;'><p></p>
        <p>O Conjunto de Dados de Jogadores de Futebol de 2017 a 2023 fornece informações abrangentes sobre jogadores de futebol profissionais. 
        O conjunto de dados contém uma ampla variedade de atributos, incluindo dados demográficos dos jogadores, características físicas, estatísticas de jogo, 
        detalhes contratuais e afiliações a clubes.</p>
        <p><b>Com mais de 17.000 registros</b>, este conjunto de dados oferece um recurso valioso para analistas de futebol, 
        pesquisadores e entusiastas interessados em explorar diversos aspectos do mundo do futebol, pois permite estudar atributos dos jogadores, 
        métricas de desempenho, avaliação de mercado, análise de clubes, posicionamento dos jogadores e seu desenvolvimento ao longo do tempo.</p>
    </div>
    """,
    unsafe_allow_html=True
)