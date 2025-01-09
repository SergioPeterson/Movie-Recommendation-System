import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from priv.constants import PASSWORD  

# Load the cleaned data
cleaned_data = pd.read_csv("cleaned_movie_data.csv")

# Split the data into Movies and Ratings DataFrames
movies = cleaned_data[['movieId', 'title', 'genres']].drop_duplicates(subset='movieId')
ratings = cleaned_data[['userId', 'movieId', 'rating', 'timestamp']]

# Generate dummy Users data
users = pd.DataFrame({'user_id': ratings['userId'].unique()})
users['name'] = users['user_id'].apply(lambda x: f"User{x}")
users['email'] = users['user_id'].apply(lambda x: f"user{x}@example.com")

# Convert genres from string to list
movies['genres'] = movies['genres'].apply(eval)

# Ensure all datatypes are converted to native Python types
movies['movieId'] = movies['movieId'].astype(int)
ratings['userId'] = ratings['userId'].astype(int)
ratings['movieId'] = ratings['movieId'].astype(int)
ratings['rating'] = ratings['rating'].astype(float)
ratings['timestamp'] = ratings['timestamp'].astype(int)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="moviedb", user="postgres", password=PASSWORD, host="localhost"
)
cursor = conn.cursor()

# Clear existing data in the tables
cursor.execute("TRUNCATE TABLE Ratings CASCADE;")
cursor.execute("TRUNCATE TABLE Movies CASCADE;")
cursor.execute("TRUNCATE TABLE Users CASCADE;")

# Insert Users
users_to_insert = [
    (int(row.user_id), row.name, row.email) for _, row in users.iterrows()
]
execute_values(
    cursor,
    """
    INSERT INTO Users (user_id, name, email)
    VALUES %s
    ON CONFLICT (user_id) DO NOTHING
    """,
    users_to_insert
)

# Insert Movies
movies_to_insert = [
    (int(row.movieId), row.title, row.genres) for _, row in movies.iterrows()
]
execute_values(
    cursor,
    """
    INSERT INTO Movies (movie_id, title, genres)
    VALUES %s
    ON CONFLICT (movie_id) DO NOTHING
    """,
    movies_to_insert
)

# Insert Ratings
ratings_to_insert = [
    (int(row.userId), int(row.movieId), float(row.rating), int(row.timestamp))
    for _, row in ratings.iterrows()
]
execute_values(
    cursor,
    """
    INSERT INTO Ratings (user_id, movie_id, rating, timestamp)
    VALUES %s
    ON CONFLICT DO NOTHING
    """,
    ratings_to_insert
)

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Data successfully loaded into the database!")