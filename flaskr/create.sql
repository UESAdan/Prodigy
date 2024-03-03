DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS kids;


CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    -- Add other user fields as needed
);


CREATE TABLE kids(
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    profession TEXT NOT NULL,
    age INTEGER,
    location TEXT NOT NULL,
    programs TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, name, profession) -- Ensures each combination of user_id, name, and profession is unique
);
