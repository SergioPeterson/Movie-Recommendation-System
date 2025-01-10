import psycopg2
import pandas as pd
from elasticsearch import Elasticsearch, helpers

# Fetch movies data from PostgreSQL
def fetch_movies_from_db():
    conn = psycopg2.connect(
        dbname="moviedb", user="postgres", password="Elpanzon#1", host="localhost"
    )
    query = "SELECT movie_id AS movieId, title, genres FROM Movies;"
    movies = pd.read_sql_query(query, conn)
    conn.close()
    # Convert genres (list) to a string for Elasticsearch
    movies['genres'] = movies['genres'].apply(lambda x: ', '.join(eval(x)) if x else '')
    return movies

# Connect to Elasticsearch
try:
    es = Elasticsearch(hosts=["http://localhost:9200"])
    if not es.ping():
        raise ValueError("Elasticsearch connection failed! Make sure Elasticsearch is running.")
    print("Connected to Elasticsearch.")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Fetch movies data
movies = fetch_movies_from_db()

# Index movies into Elasticsearch
movies_data = movies.to_dict(orient='records')
actions = [
    {
        "_index": "movies",
        "_id": movie['movieId'],
        "_source": movie
    }
    for movie in movies_data
]

# Bulk index movies
try:
    helpers.bulk(es, actions)
    print(f"Indexed {len(actions)} movies into Elasticsearch.")
except Exception as e:
    print(f"Error during indexing: {e}")
    exit()

# Search movies
def search_movies(query):
    try:
        response = es.search(index="movies", body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "genres"]
                }
            }
        })
        return response['hits']['hits']
    except Exception as e:
        print(f"Error during search: {e}")
        return []

# Example
if __name__ == "__main__":
    results = search_movies("Toy Story")
    print("Search Results:")
    for result in results:
        print(result['_source'])