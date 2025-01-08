import pandas as pd

# Load MovieLens datasets
movies = pd.read_csv("movies.csv")  # Ensure you have the MovieLens dataset
ratings = pd.read_csv("ratings.csv")

# Inspect datasets
print("Movies Dataset:\n", movies.head())
print("Ratings Dataset:\n", ratings.head())

# Data Cleaning
# Split genres into a list
movies['genres'] = movies['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])

# Remove duplicate ratings
ratings = ratings.drop_duplicates(subset=['userId', 'movieId'], keep='last')

# Merge datasets for analysis
merged_data = pd.merge(ratings, movies, on='movieId')
print("Merged Dataset:\n", merged_data.head())

# Save cleaned data for later use
merged_data.to_csv("cleaned_movie_data.csv", index=False)