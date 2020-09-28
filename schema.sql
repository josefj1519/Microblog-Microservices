-- $ sqlite3 microblog.db < schema.sql

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS userfollowers;
DROP TABLE IF EXISTS tweets;

CREATE TABLE users (
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    hashpass VARCHAR NOT NULL,
    UNIQUE(username, email),
    PRIMARY KEY(username)
);

CREATE TABLE userfollowers (
    followee VARCHAR NOT NULL,
    follower  VARCHAR NOT NULL,
    FOREIGN KEY(follower) REFERENCES users(username),
    FOREIGN KEY(followee) REFERENCES users(username),
    PRIMARY KEY(followee, follower)
);

CREATE TABLE tweets (
    author VARCHAR NOT NULL,
    post VARCHAR NOT NULL,
    posttimestamp DATETIME NOT NULL,
    FOREIGN KEY(author) REFERENCES users(username)
); 

-- Sample Users
INSERT INTO users(username, email, hashpass) VALUES('williamguy', 'powerpuff@hotmail.com', 'hashedpassword');
INSERT INTO users(username, email, hashpass) VALUES('jankers', 'coolguy@gmail.com', '12345');
INSERT INTO users(username, email, hashpass) VALUES('goyo123', 'patriots@outlook.com', 'racecar');

-- Sample UserFollowers
INSERT INTO userfollowers(followee, follower) VALUES('jankers', 'williamguy');
INSERT INTO userfollowers(followee, follower) VALUES('jankers', 'goyo123');
INSERT INTO userfollowers(followee, follower) VALUES('williamguy', 'goyo123');
INSERT INTO userfollowers(followee, follower) VALUES('goyo123', 'williamguy');

-- Sample tweets
INSERT INTO tweets(author, post, posttimestamp) VALUES('jankers','williamguy is a loser!', 	'2008-11-11 13:23:44');
INSERT INTO tweets(author, post, posttimestamp) VALUES('williamguy','jankers is awsome!!', 	'2008-11-11 13:22:48');
COMMIT;
