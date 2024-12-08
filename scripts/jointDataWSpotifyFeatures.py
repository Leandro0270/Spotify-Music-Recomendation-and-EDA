import pandas as pd


spotify_features = pd.read_csv('SpotifyFeatures.csv')
data = pd.read_csv('data.csv')


merged_data = pd.merge(data, spotify_features[['track_id', 'genre']], 
                       left_on='id', right_on='track_id', how='left')


merged_data.drop(columns=['track_id'], inplace=True)

merged_data.to_csv('data_with_genre.csv', index=False)

print("Coluna 'genre' adicionada com sucesso ao dataset 'data.csv'!")