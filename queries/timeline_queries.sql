-- :name user_in_database :one
select * from users where username = :username

-- :name add_user_tweet :insert
insert into tweets values (:username, :tweet, :currentTimestamp) 

-- :name get_user_tweets :many
select * from tweets where author like (:username) ORDER BY posttimestamp DESC LIMIT 25

-- :name get_followees :many
select * from userfollowers where follower like (:username)

-- :name get_followed_tweets :many
select * from tweets where author in :followees ORDER BY posttimestamp DESC LIMIT 25

-- :name get_all_tweets :many
select * from tweets ORDER BY posttimestamp DESC LIMIT 25