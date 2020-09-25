-- :name add_user_tweet :insert
insert into tweets values (:tweet) 

-- :name get_user_tweets :many
select * from tweets where author like :username

-- :name get_followed_tweets: :many
select * from tweets where author in (:followees)

-- :name get_all_tweets :many
select * from tweets 