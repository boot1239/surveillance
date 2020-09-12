create table citizen (
    id serial primary key,
    first_name varchar not null,
    last_name varchar not null,
    citizen_id integer not null unique,
    gender varchar not null,
    birthdate varchar not null,
    address varchar not null,
    current_location varchar not null
);