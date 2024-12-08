import pandas as pd


file_path = "refined_data.csv"
data = pd.read_csv(file_path)


columns_to_average = [
    "valence", "acousticness", "danceability", "duration_ms", "energy", 
    "instrumentalness", "key", "liveness", "loudness", "mode", 
    "popularity", "speechiness"
]


grouped_data = data.groupby("genre").agg({**{col: 'mean' for col in columns_to_average}, 'genre': 'size'}).rename(columns={"genre": "count"}).reset_index()

output_file = "grouped_by_genre.csv"
grouped_data.to_csv(output_file, index=False)

print(grouped_data.head())