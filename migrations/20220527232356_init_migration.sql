

-- +goose Up
-- +goose StatementBegin
create table category
(
    id bigint primary key,
    title varchar not null
);

create table theme
(
    id bigint primary key,
    category_id bigint references category,
    title varchar not null
);

create table appeal
(
    id bigserial primary key,
    text varchar not null,
    detailed_text varchar,
    confirmed_theme bigint references theme
);

create table appeal_has_theme
(
    id bigserial primary key,
    order_number integer not null,
    appeal_id bigint references appeal,
    theme_id bigint references theme
);
-- +goose StatementEnd



-- +goose Down
-- +goose StatementBegin
drop table if exists appeal_has_theme;
drop table if exists appeal;
drop table if exists theme;
drop table if exists category;
-- +goose StatementEnd
