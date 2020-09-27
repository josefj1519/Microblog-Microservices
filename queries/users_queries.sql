-- :name all_users :many
select * from users;

-- :name look_for_user :one
select username, email from users where username = :username or email := email

-- :name create_user :insert
insert into users (username, email, hashpass) values (:username, :email, :hashpass)

-- :name authenticate_user :many
select username from users where (username = :username and hashpass = :hashpass)