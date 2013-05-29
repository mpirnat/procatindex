drop table if exists cats;
create table cats (
    id integer primary key,
    title text not null,
    created text not null -- ISO8601 date string: "YYYY-MM-DD HH:MM:SS.SSS"
);
