import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import os

st.set_page_config(
    page_title='Teams',
    page_icon='⚽',
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

df_filtered = df_data[df_data['Club'] == club].set_index('Name')

# ⚽ pega URL e cria um ID único para o time
foto_url = str(df_filtered.iloc[0]['Club Logo']).strip()
#club_id = str(df_filtered.iloc[0]['Club'])
club_id = str(df_filtered.iloc[0]['Club']).replace(" ", "_")

# pega imagem local (ou baixa se não existir)
local_path = get_local_image_path(foto_url, club_id)
if local_path and os.path.exists(local_path):
    st.image(local_path)
else:
    st.warning("Imagem não disponível.")
st.markdown(f"## {club}")

columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined',
           'Height(cm.)', 'Weight(lbs.)',
           'Contract Valid Until', 'Release Clause(£)']

st.dataframe(df_filtered[columns],
             column_config={
                 "Overall": st.column_config.ProgressColumn("Overall", min_value=0, max_value=100, format="%d"),
                 "Wage(£)": st.column_config.ProgressColumn("Wage(£)", min_value=0, max_value=df_filtered['Wage(£)'].max(), format="£%f"),
                 "Photo": st.column_config.ImageColumn(),
                 "Flag": st.column_config.ImageColumn('Country')
             }
             )