-- name: get_users
-- Get all the users in the database
select
    *
from
    users;

-- name: create_user<!
-- Create a user in the database
insert into
    users (email, password)
values
    (:email, :password);

-- name: get_user_by_credentials^
-- Verify login credentials and return user
select
    *
from
    users
where
    email = :email
    and password = :password;

-- name: get_user_by_id^
-- Get a user by id
select
    *
from
    users
where
    id = :id;