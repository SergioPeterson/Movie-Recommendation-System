from elasticsearch import Elasticsearch, helpers

# Connect to Elasticsearch
es = Elasticsearch()

# Index movies
movies_data = movies.to_dict(orient='records')
actions = [
    {
        "_index": "movies",
        "_id": movie['movieId'],
        "_source": movie
    }
    for movie in movies_data
]
helpers.bulk(es, actions)

# Search movies
def search_movies(query):
    response = es.search(index="movies", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "genres"]
            }
        }
    })
    return response['hits']['hits']

# Example
print(search_movies("Toy Story"))