import pandas as pd


data_with_genre = pd.read_csv("data_with_genre_transformed.csv")
spotify_data = pd.read_csv("spotify_data_cleaned.csv")


data_with_genre = data_with_genre[data_with_genre['genre'].notna() & (data_with_genre['genre'] != '')]
spotify_data = spotify_data[spotify_data['genre'].notna() & (spotify_data['genre'] != '')]


spotify_data = spotify_data[data_with_genre.columns]


combined_data = pd.concat([data_with_genre, spotify_data], ignore_index=True)


combined_data = combined_data.sort_values(by=['track_id', 'genre'], ascending=[True, True])
refined_data = combined_data.drop_duplicates(subset='track_id', keep='last')


refined_data['genre'] = refined_data['genre'].str.lower()


refined_data.to_csv("refined_data.csv", index=False)

print("Processo concluído! O arquivo refined_data.csv foi salvo.")