from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split, accuracy

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
print("RMSE: ", accuracy.rmse(predictions))

# Get recommendations for a user
def get_recommendations(user_id, top_n=10):
    all_movies = ratings['movieId'].unique()
    user_movies = ratings[ratings['userId'] == user_id]['movieId'].values
    recommendations = [
        (movie, algo.predict(user_id, movie).est)
        for movie in all_movies if movie not in user_movies
    ]
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]
    return recommendations

# Example
print(get_recommendations(user_id=1))