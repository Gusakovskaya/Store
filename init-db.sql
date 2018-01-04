\c store
CREATE TABLE IF NOT EXISTS store_user (
    id                  serial primary key,
    email               varchar(254),
    avatar              varchar(64),
    shipping_adress     varchar(64),
    credits             integer DEFAULT 0,
    role                varchar(32)
);
