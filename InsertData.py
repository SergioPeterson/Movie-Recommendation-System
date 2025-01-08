import psycopg2
from psycopg2.extras import execute_values

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="moviedb", user="postgres", password="yourpassword", host="localhost"
)
cursor = conn.cursor()

# Insert Movies
movies_to_insert = [
    (row.movieId, row.title, row.genres, None, None)
    for _, row in movies.iterrows()
]
execute_values(cursor, "INSERT INTO Movies (movie_id, title, genres) VALUES %s", movies_to_insert)

# Insert Ratings
ratings_to_insert = [
    (row.userId, row.movieId, row.rating, row.timestamp)
    for _, row in ratings.iterrows()
]
execute_values(cursor, "INSERT INTO Ratings (user_id, movie_id, rating, timestamp) VALUES %s", ratings_to_insert)

# Commit and close
conn.commit()
cursor.close()
conn.close()