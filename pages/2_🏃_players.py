import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import os

st.set_page_config(
    page_title='Players',
    page_icon='🏃',
    layout='wide'
)

# cria pasta local se não existir
os.makedirs("images", exist_ok=True)
def get_local_image_path(url: str, player_id: str) -> str:
    """Retorna o caminho local da imagem, baixando se necessário"""
    # nome do arquivo local (ex: images/177003.png)
    local_path = f"images/{player_id}.png"

    if not os.path.exists(local_path):  
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://sofifa.com"  # força aceitar o download
            }
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(r.content)
        except Exception as e:
            st.error(f"Erro ao baixar imagem: {e}")
            return None
    return local_path

df_data = st.session_state["data"]

clubs = df_data['Club'].value_counts().index
club = st.sidebar.selectbox('Clube', clubs)

df_players = df_data[df_data['Club'] == club]
players = df_players['Name'].value_counts().index
player = st.sidebar.selectbox('Jogador', players)

player_stats = df_players[df_players['Name'] == player].iloc[0]


# ⚽ pega URL e cria um ID único para o jogador
foto_url = str(player_stats['Photo']).strip()
player_id = str(player_stats['ID']) if 'ID' in player_stats else str(player_stats['Name']).replace(" ", "_")

# pega imagem local (ou baixa se não existir)
local_path = get_local_image_path(foto_url, player_id)

if local_path and os.path.exists(local_path):
    st.image(local_path)
else:
    st.warning("Imagem não disponível.")

st.title(str(player_stats['Name']))
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100}")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)'] * 0.453:.2f}")
st.divider()
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats['Overall']))

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor de mercado", value=f"£ {player_stats['Value(£)']:,}")
col2.metric(label="Remuneração mensal", value=f"£ {player_stats['Wage(£)'] * 4:,}")
col3.metric(label="Cláusula de rescisão", value=f"£ {player_stats['Release Clause(£)']:,}")
