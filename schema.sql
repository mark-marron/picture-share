DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (username, password)
VALUES("admin", "password")

SELECT *
FROM users;

###################################

DROP TABLE IF EXISTS posts;

CREATE TABLE posts
(
  image_id TEXT NOT NULL PRIMARY KEY,
  user_id INTEGER,
  timestamp TEXT NOT NULL,
  caption TEXT
);

SELECT *
FROM posts;