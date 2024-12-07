import pandas as pd


file_path = "data_with_genre.csv"
df = pd.read_csv(file_path)


df['artists'] = df['artists'].apply(lambda x: " & ".join(eval(x)))

df = df.drop(columns=['release_date', 'explicit'])


df.to_csv("data_with_genre_transformed.csv", index=False)
print(df.head())