import pandas as pd


file_path = 'spotify_data.csv' 
data = pd.read_csv(file_path)


columns_to_remove = ['index', 'time_signature']
data_cleaned = data.drop(columns=columns_to_remove, errors='ignore')


output_file = 'spotify_data_cleaned.csv'
data_cleaned.to_csv(output_file, index=False)

print(f"Dataset limpo salvo como {output_file}.")