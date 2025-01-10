Movie Recommendation System

Project Overview

This project is a Movie Recommendation System that combines machine learning, database management, and search indexing to provide personalized movie recommendations. It leverages user ratings to recommend movies using collaborative filtering and indexes movie metadata for efficient fuzzy searching through Elasticsearch.

Key Features
	1.	Personalized Recommendations:
	•	Recommends movies to users based on their past ratings using the SVD (Singular Value Decomposition) algorithm.
	•	Supports hybrid collaborative filtering.
	2.	Search Functionality:
	•	Allows users to search for movies by title or genres with fuzzy matching using Elasticsearch.
	3.	Rating System:
	•	Users can rate movies, and the database is updated in real-time.
	4.	Database Integration:
	•	Uses PostgreSQL for managing movies, users, and ratings data.
	5.	Scalable Design:
	•	Employs Elasticsearch for fast and scalable movie search.

Key Tools and Technologies
	1.	Python:
	•	pandas: Data manipulation and preprocessing.
	•	scikit-surprise: Machine learning library for collaborative filtering.
	•	Flask: Backend web framework for serving API endpoints.
	•	psycopg2: PostgreSQL database interaction.
	•	Elasticsearch Python Client: Indexing and searching movies.
	2.	PostgreSQL:
	•	Relational database for storing user ratings and movie metadata.
	3.	Elasticsearch:
	•	Search engine for fuzzy search and efficient movie metadata retrieval.
	4.	Docker (Optional):
	•	Containerizes the application for consistent and reproducible deployment.

System Architecture
	1.	Database Layer:
	•	Stores and manages user, movie, and rating data using PostgreSQL.
	2.	Recommendation Layer:
	•	Utilizes SVD (Singular Value Decomposition) for collaborative filtering.
	•	Fetches and preprocesses data from the PostgreSQL database.
	3.	Search Layer:
	•	Indexes movie metadata in Elasticsearch for fast and accurate search results.
	4.	Web Layer:
	•	Provides REST API endpoints via Flask for searching movies and submitting ratings.

Setup Instructions

1. Clone the Repository

git clone https://github.com/your-repo/Movie-Recommendation-System.git
cd Movie-Recommendation-System

2. Set Up a Virtual Environment

python -m venv movie-recommender-env
source movie-recommender-env/bin/activate  # On Windows: movie-recommender-env\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Set Up PostgreSQL

Step 4.1: Create the Database

CREATE DATABASE moviedb;

Step 4.2: Create Tables

Run the schema.sql file:

psql -U postgres -d moviedb -f schema.sql

Step 4.3: Load Initial Data

Use the load_data_to_db.py script to populate the database:

python load_data_to_db.py

5. Set Up Elasticsearch

Step 5.1: Install Elasticsearch
	•	Install Elasticsearch via Homebrew or Download Page.

Step 5.2: Start Elasticsearch

elasticsearch

Step 5.3: Index Movie Data

Run the elasticsearch_setup.py script:

python elasticsearch_setup.py

6. Start the Flask App

Run the app.py script:

python app.py

7. Access the Application

Endpoints
	1.	Recommendations:
	•	Endpoint: GET /recommend
	•	Parameters: user_id
	•	Example:

curl "http://127.0.0.1:5000/recommend?user_id=1"


	2.	Search Movies:
	•	Endpoint: GET /search
	•	Parameters: query
	•	Example:

curl "http://127.0.0.1:5000/search?query=Toy Story"


	3.	Rate a Movie:
	•	Endpoint: POST /rate
	•	Payload:

{
    "user_id": 1,
    "movie_id": 100,
    "rating": 4.5
}


	•	Example:

curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "movie_id": 100, "rating": 4.5}' "http://127.0.0.1:5000/rate"

Key Metrics
	1.	Recommendation Performance:
	•	Evaluated using Root Mean Square Error (RMSE) on the test set.
	•	Example RMSE: ~0.85 (depends on dataset).
	2.	Search Efficiency:
	•	Elasticsearch provides sub-second query performance on movie metadata.
	3.	Database Scalability:
	•	PostgreSQL optimized for handling large datasets of users, movies, and ratings.

Project Structure

Movie-Recommendation-System/
├── app.py                  # Flask API
├── recommender.py          # Recommendation logic
├── elasticsearch_setup.py  # Elasticsearch setup
├── load_data_to_db.py      # Database setup and data loading
├── schema.sql              # SQL schema for PostgreSQL
├── priv/                   # Sensitive constants (e.g., passwords)
│   └── constants.py
├── ml-32m/                 # Raw datasets (MovieLens)
├── templates/              # HTML templates for optional frontend
│   ├── index.html
│   └── loading.html
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

Future Improvements
	1.	Model Enhancements:
	•	Add content-based filtering or hybrid recommendation models.
	•	Experiment with deep learning models (e.g., Autoencoders).
	2.	Frontend Development:
	•	Build a React.js or Vue.js frontend for a more user-friendly interface.
	3.	Scalability:
	•	Dockerize the application for consistent deployment.
	•	Use Kubernetes to orchestrate the services.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Let me know if you’d like help refining this further or customizing it to specific requirements!
