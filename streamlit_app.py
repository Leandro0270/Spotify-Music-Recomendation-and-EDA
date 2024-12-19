from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cdist
import streamlit as st
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = ""
CLIENT_SECRET = ""
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))


@st.cache_data
def load_data():
    data = pd.read_csv("refined_data.csv")
    
    numeric_cols = [
        'valence', 'acousticness', 'danceability', 'duration_ms',
        'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'popularity', 'speechiness', 'tempo'
    ]
    
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data.fillna(0, inplace=True)

    le = LabelEncoder()
    data['genre_encoded'] = le.fit_transform(data['genre'].fillna('Unknown Genre'))
    numeric_cols.append('genre_encoded')

    data['track_name'] = data['track_name'].fillna('Unknown Track').astype(str)
    data['artists'] = data['artists'].fillna('Unknown Artist').astype(str)
    data['display_name'] = data['track_name'] + " - " + data['artists'] + " (" + data['year'].astype(int).astype(str) + ")"
    
    return data, numeric_cols

data, numeric_cols = load_data()

@st.cache_resource
def setup_knn(data, numeric_cols, n_neighbors=10):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data[numeric_cols])
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean').fit(scaled_data)
    return data, scaler, knn

data, scaler, knn = setup_knn(data, numeric_cols)

def get_album_cover(song_name, artist_name):
    """Buscar a capa do álbum no Spotify."""
    try:
        results = sp.search(q=f"track:{song_name} artist:{artist_name}", type="track", limit=1)
        if results and results["tracks"]["items"]:
            album_cover_url = results["tracks"]["items"][0]["album"]["images"][0]["url"]
            return album_cover_url
        else:
            return "https://i.postimg.cc/0QNxYz4V/social.png" 
    except Exception as e:
        st.warning(f"Erro ao buscar capa do álbum: {e}")
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def get_song_data(song_name, data):
    try:
        return data[data['display_name'] == song_name].iloc[0]
    except IndexError:
        return None

def get_mean_vector(song_list, data, numeric_cols):
    vectors = []
    for song_name in song_list:
        song_data = get_song_data(song_name, data)
        if song_data is None:
            continue
        vector = song_data[numeric_cols].values
        vectors.append(vector)
    if not vectors:
        raise ValueError("Nenhuma música válida selecionada para a recomendação.")
    return np.mean(vectors, axis=0)

def recommend_songs_knn(song_list, data, scaler, numeric_cols, knn, n_neighbors=10):
    mean_vector = get_mean_vector(song_list, data, numeric_cols)
    scaled_mean_vector = scaler.transform([mean_vector])
    distances, indices = knn.kneighbors(scaled_mean_vector)
    recommendations = data.iloc[indices[0]].copy()
    recommendations['distance'] = distances[0]
    return filter_recommendations(song_list, recommendations, n_neighbors)

def filter_recommendations(song_list, recommendations, n_songs):
    filtered_recommendations = recommendations[~recommendations['display_name'].isin(song_list)].copy()
    
    if len(filtered_recommendations) > 5:
        filtered_recommendations = filtered_recommendations.sample(5)
    return filtered_recommendations[['track_name', 'artists', 'year', 'genre']]


if "selected_songs" not in st.session_state:
    st.session_state.selected_songs = []


st.title("Recomendação de Músicas 🎵")
search_query = st.text_input("Digite o nome da música ou artista:")

if search_query:
    search_results = data[data['display_name'].str.contains(search_query, case=False, na=False)]
    if not search_results.empty:
        selected_song = st.selectbox("Selecione uma música:", options=search_results['display_name'])
    else:
        selected_song = None
        st.write("Nenhuma música encontrada.")
else:
    selected_song = None


if selected_song and st.button("Adicionar música"):
    if selected_song not in st.session_state.selected_songs:
        st.session_state.selected_songs.append(selected_song)
        st.success(f"Música adicionada: {selected_song}")
    else:
        st.warning("A música já está na lista.")


st.subheader("Músicas Selecionadas:")
if st.session_state.selected_songs:
    for song in st.session_state.selected_songs:
        st.write(f"- {song}")
else:
    st.write("Nenhuma música adicionada ainda.")


if st.session_state.selected_songs:
    if st.button("Recomendar músicas"):
        try:
            recommendations = recommend_songs_knn(
                st.session_state.selected_songs,
                data,
                scaler,
                numeric_cols,
                knn
            )
            st.subheader("Recomendações:")
            for _, row in recommendations.iterrows():
                album_cover = get_album_cover(row['track_name'], row['artists'])
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(album_cover, width=150)
                with col2:
                    st.write(f"**{row['track_name']}**")
                    st.write(f"{row['artists']} ({row['year']})")
                    st.write(f"Gênero: {row['genre']}")
        except ValueError as e:
            st.error(str(e))