-- :name all_users :many
select * from users;

-- :name check_for_user :scalar
select username from users where username = :username

-- :name create_user :insert
insert into users (username, email, hashpass) values (:username, :email, :hashpass)

-- :name authenticate_user :many
select username from users where (username = :username and hashpass = :hashpass)

-- :name check_users_followers :many
select follower from userfollowers where followee = :followee

-- :name check_following_users :many
select followee from userfollowers where follower = :follower

-- :name start_following_user :insert
insert into userfollowers (followee, follower) values (:followee, :follower)

-- :name stop_following 
delete from userfollowers where followee = :followee and follower = :follower