import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import random

# Carregar dados
@st.cache_data
def load_data():
    data = pd.read_csv("/workspaces/mtad-spotify-data-analysis/datasets/refined_data.csv")
    
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
    return data

data = load_data()

# Configurar KMeans
@st.cache_resource
def setup_kmeans(data):
    number_cols = [
        'valence', 'acousticness', 'danceability', 'duration_ms',
        'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'popularity', 'speechiness', 'tempo', 'year'
    ]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[number_cols].fillna(0))
    kmeans = KMeans(n_clusters=20, random_state=42).fit(scaled_data)
    data['cluster_label'] = kmeans.predict(scaled_data)
    return data, scaler, kmeans, number_cols

data, scaler, kmeans, number_cols = setup_kmeans(data)

# Funções de Recomendação
def get_song_data(song_name, data):
    try:
        return data[data['display_name'] == song_name].iloc[0]
    except IndexError:
        return None

def get_mean_vector(song_list, data, scaler, number_cols):
    vectors = []
    for song_name in song_list:
        song_data = get_song_data(song_name, data)
        if song_data is None:
            continue
        vector = song_data[number_cols].values
        vectors.append(vector)
    if not vectors:
        raise ValueError("Nenhuma música válida selecionada para a recomendação.")
    return np.mean(vectors, axis=0)

def recommend_songs(song_list, data, scaler, number_cols, n_songs=10):
    mean_vector = get_mean_vector(song_list, data, scaler, number_cols)
    song_matrix = scaler.transform(data[number_cols].fillna(0))
    distances = cdist([mean_vector], song_matrix, metric='cosine')[0]
    data['distance'] = distances
    recommendations = data.sort_values('distance').head(n_songs)
    return recommendations[['track_name', 'artists', 'year']]

# Estado da sessão para armazenar músicas selecionadas
if "selected_songs" not in st.session_state:
    st.session_state.selected_songs = []

# Interface Streamlit
st.title("Recomendação de Músicas 🎵")

# Campo de busca
search_query = st.text_input("Digite o nome da música ou artista:")
if search_query:
    search_results = data[data['display_name'].str.contains(search_query, case=False, na=False)]
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

# Botão para adicionar música
if selected_song and st.button("Adicionar música"):
    if selected_song not in st.session_state.selected_songs:
        st.session_state.selected_songs.append(selected_song)
        st.success(f"Música adicionada: {selected_song}")
    else:
        st.warning("A música já está na lista.")

# Mostrar músicas selecionadas
st.subheader("Músicas Selecionadas:")
if st.session_state.selected_songs:
    for song in st.session_state.selected_songs:
        st.write(f"- {song}")
else:
    st.write("Nenhuma música adicionada ainda.")

# Botão para recomendar músicas
if st.session_state.selected_songs:
    if st.button("Recomendar músicas"):
        try:
            recommendations = recommend_songs(
                st.session_state.selected_songs,
                data,
                scaler,
                number_cols
            )
            st.subheader("Recomendações:")
            random_recommendations = recommendations.sample(5)
            for i, row in random_recommendations.iterrows():
                st.write(f"- {row['track_name']} - {row['artists']} ({row['year']})")
        except ValueError as e:
            st.error(str(e))