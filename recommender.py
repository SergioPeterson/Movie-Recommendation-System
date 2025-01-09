import psycopg2
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from priv.constants import PASSWORD  

# Connect to the PostgreSQL database and fetch ratings
def fetch_ratings_from_db():
    conn = psycopg2.connect(
        dbname="moviedb", user="postgres", password=PASSWORD, host="localhost"
    )
    query = """
    SELECT user_id AS userId, movie_id AS movieId, rating
    FROM Ratings;
    """
    ratings = pd.read_sql_query(query, conn)
    conn.close()
    return ratings

# Connect to the PostgreSQL database and fetch movie titles
def fetch_movies_from_db():
    conn = psycopg2.connect(
        dbname="moviedb", user="postgres", password=PASSWORD, host="localhost"
    )
    query = """
    SELECT movie_id AS movieId, title
    FROM Movies;
    """
    movies = pd.read_sql_query(query, conn)
    conn.close()
    return movies

# Fetch ratings and movies from the database
ratings = fetch_ratings_from_db()
movies = fetch_movies_from_db()

# Ensure column names are correct
ratings.columns = ['userId', 'movieId', 'rating']  # Explicit renaming, if needed
movies.columns = ['movieId', 'title']  # Ensure movieId and title columns are present

# Load data into Surprise
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Train-test split
trainset, testset = train_test_split(data, test_size=0.2)

# Train SVD model
algo = SVD()
algo.fit(trainset)

# Evaluate the model
predictions = algo.test(testset)
# print("RMSE: ", accuracy.rmse(predictions))

# Get recommendations for a user
def get_recommendations(user_id, top_n=10):
    all_movies = ratings['movieId'].unique()
    user_movies = ratings[ratings['userId'] == user_id]['movieId'].values
    recommendations = [
        (movie, algo.predict(user_id, movie).est)
        for movie in all_movies if movie not in user_movies
    ]
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]
    
    # Map movieId to titles
    movie_map = dict(zip(movies['movieId'], movies['title']))
    recommendations_with_titles = [
        (movie_map.get(movie, "Unknown"), score) for movie, score in recommendations
    ]
    return recommendations_with_titles

# Example
if __name__ == "__main__":
    print("Starting Recommender")
    print(get_recommendations(user_id=1))