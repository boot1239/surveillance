create table citizen (
    id serial primary key,
    first_name varchar not null,
    last_name varchar not null,
    citizen_id varchar not null unique,
    gender integer not null,
    gender_name varchar not null,
    sector varchar not null,
    birthdate varchar not null,
    position integer[]
);