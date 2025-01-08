from flask import Flask, request, jsonify

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
    # Add to the database (pseudo-code)
    # save_rating_to_db(user_id, movie_id, rating)
    return jsonify({'message': 'Rating submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)