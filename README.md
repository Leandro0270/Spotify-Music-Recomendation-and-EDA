# Spotify Data Analysis and Music Recommendation System 🎵

This repository showcases a project involving exploratory data analysis (EDA) on Spotify datasets and the implementation of a music recommendation system using a K-Nearest Neighbors (KNN) model deployed with [Streamlit](https://streamlit.io/).

## 📋 Overview

- **Datasets Used:**
  - [Ultimate Spotify Tracks DB](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db)
  - [Spotify Dataset](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset)
  - [Spotify Artists and Tracks Datasets](https://www.kaggle.com/datasets/gokulraja84/spotify-artists-and-tracks-datasets)
- **Key Features:**
  - Merging and cleaning data from multiple datasets.
  - Exploratory Data Analysis (EDA) to uncover trends and patterns in Spotify data.
  - Building a music recommendation system using a KNN model.
  - Interactive web app built with Streamlit for music recommendations.
- **Tech Stack:**
  - Python (Pandas, Scikit-learn, Plotly, etc.)
  - Docker (with GPU support for KNN training)
  - Streamlit (for the user interface)

## 📊 Exploratory Data Analysis

The EDA explores various features such as:
- Trends in song durations, loudness, and energy over the years.
- Genre popularity and average song attributes.
- Correlation analysis between numeric features.

Some visualizations include:
- Heatmaps to show correlations.
- Bar plots for genre popularity and song duration.
- Clustering of genres and songs using t-SNE and K-means.

## 🛠️ Music Recommendation System

The recommendation system leverages a KNN model trained on Spotify track features. Key steps:
1. Data Preprocessing:
   - Standardization of numeric features.
   - Feature selection based on their importance and correlation.
2. Model Training:
   - Optimal parameters for KNN (e.g., `n_neighbors`) were determined using cross-validation.
   - Training and evaluation of the KNN model using GPU acceleration with Docker.
3. Recommendations:
   - Songs similar to a given input are retrieved using the trained KNN model.

## 🚀 Getting Started

### Running the Streamlit App 

You don't need to use Docker to run the Streamlit app. You can run it directly in your local Python environment by following these steps:

1. **Install Python Dependencies:**

   Make sure you have Python installed (preferably version 3.8 or later). Install the required dependencies using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt

    Set Up Spotify API Credentials:

    Open the file streamlit_app.py and add your Spotify API credentials in the following fields:

CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"

    You can get your Spotify API credentials from Spotify Developer.

Run the Streamlit App:

Start the Streamlit application by running the following command:

    streamlit run streamlit_app.py

    Access the App:

    Open your browser and go to http://localhost:8501 to interact with the application.

📈 Results

The project highlights:

    Insights generated from Spotify data trends.
    An efficient recommendation system based on KNN.
    An interactive interface for exploring and discovering new music.