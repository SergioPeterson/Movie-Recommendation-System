CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE Movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255),
    genres TEXT[],
    description TEXT,
    year INT
);

CREATE TABLE Ratings (
    user_id INT,
    movie_id INT,
    rating FLOAT,
    timestamp BIGINT,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);