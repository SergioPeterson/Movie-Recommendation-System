from flask import Flask, request, jsonify
from recommender import get_recommendations
import psycopg2
from priv.constants import PASSWORD  

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = int(request.args.get('user_id'))
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)

@app.route('/rate', methods=['POST'])
def rate_movie():
    data = request.json
    user_id = data['user_id']
    movie_id = data['movie_id']
    rating = data['rating']

    # Add the new rating to the database
    try:
        conn = psycopg2.connect(
            dbname="moviedb", user="postgres", password=PASSWORD, host="localhost"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Ratings (user_id, movie_id, rating, timestamp) VALUES (%s, %s, %s, EXTRACT(EPOCH FROM NOW()))",
            (user_id, movie_id, rating)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Rating submitted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)