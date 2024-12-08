import streamlit as st
import pandas as pd
import time

# Carregar dados
@st.cache_data
def load_data():
    data = pd.read_csv("../datasets/refined_data.csv")
    
    # Garantir que colunas numéricas sejam tratadas corretamente
    feature_names = [
        'year', 'danceability', 'energy', 'loudness', 'mode', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness', 'valence', 'duration_ms'
    ]
    for feature in feature_names:
        data[feature] = pd.to_numeric(data[feature], errors='coerce')
    data.fillna('', inplace=True)  # Preencher valores ausentes com strings vazias
    
    # Garantir que track_name e artists sejam strings
    data['track_name'] = data['track_name'].fillna('Unknown Track').astype(str)
    data['artists'] = data['artists'].fillna('Unknown Artist').astype(str)
    
    # Criar uma coluna com o formato desejado
    data['display_name'] = data['track_name'] + " - " + data['artists'] + " (" + data['year'].astype(str) + ")"
    return data[['track_name', 'artists', 'year', 'display_name']]

data = load_data()

# Inicializar lista de músicas selecionadas no estado da sessão
if "selected_songs" not in st.session_state:
    st.session_state.selected_songs = []

# Função para buscar músicas
def search_songs(query, data):
    if query:
        return data[data['display_name'].str.contains(query, case=False, na=False)]
    return data

# Interface Streamlit
st.title("Recomendação de Músicas 🎵")

# Campo de entrada com temporizador
search_query = st.text_input("Digite o nome da música ou artista:")

# Adicionar busca após 2 segundos de inatividade
if search_query:
    time.sleep(2)  # Simula inatividade
    search_results = search_songs(search_query, data)
    if not search_results.empty:
        selected_song = st.selectbox(
            "Selecione uma música:",
            options=search_results['display_name']
        )
    else:
        selected_song = None
        st.write("Nenhuma música encontrada.")
else:
    selected_song = None

# Botão para adicionar a música selecionada
if selected_song and st.button("Adicionar música"):
    if selected_song not in st.session_state.selected_songs:
        st.session_state.selected_songs.append(selected_song)
        st.success(f"Música adicionada: {selected_song}")
    else:
        st.warning("A música já está na lista.")

# Mostrar lista de músicas selecionadas
st.subheader("Músicas Selecionadas:")
if st.session_state.selected_songs:
    for song in st.session_state.selected_songs:
        st.write(f"- {song}")
else:
    st.write("Nenhuma música adicionada ainda.")

# Botão para recomendar músicas
if st.session_state.selected_songs:
    if st.button("Recomendar músicas"):
        st.write("Recomendação de músicas ainda não implementada.")