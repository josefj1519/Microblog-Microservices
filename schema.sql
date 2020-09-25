-- $ sqlite3 microblog.db < schema.sql

BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS userfollowers;
DROP TABLE IF EXISTS tweets;

CREATE TABLE users (
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    hashpass VARCHAR NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE userfollowers (
    followee VARCHAR NOT NULL,
    follower  VARCHAR NOT NULL,
    FOREIGN KEY(follower) REFERENCES users(username),
    FOREIGN KEY(followee) REFERENCES users(username)
);

CREATE TABLE tweets (
    author VARCHAR NOT NULL,
    post VARCHAR NOT NULL,
    posttimestamp DATETIME NOT NULL,
    FOREIGN KEY(author) REFERENCES users(username)
); 

-- Sample Users
INSERT INTO users(username, email, hashpass) VALUES('williamguy', 'powerpuff@hotmail.com', '$52DAF');
INSERT INTO users(username, email, hashpass) VALUES('jankers', 'coolguy@gmail.com', '#$#32F');
INSERT INTO users(username, email, hashpass) VALUES('goyo123', 'patriots@outlook.com', '#$@356');

-- Sample UserFollowers
INSERT INTO userfollowers(followee, follower) VALUES('jankers', 'williamguy');
INSERT INTO userfollowers(followee, follower) VALUES('jankers', 'goyo123');
INSERT INTO userfollowers(followee, follower) VALUES('williamguy', 'goyo123');
INSERT INTO userfollowers(followee, follower) VALUES('goyo123', 'williamguy');

-- Sample tweets
INSERT INTO tweets(author, post, posttimestamp) VALUES('jankers','williamguy is a loser!', 	'2008-11-11 13:23:44');
INSERT INTO tweets(author, post, posttimestamp) VALUES('williamguy','jankers is awsome!!', 	'2008-11-11 13:22:48');
COMMIT;
