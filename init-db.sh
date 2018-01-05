#!/usr/bin/env bash

PGPASSWORD=zhenya psql -v ON_ERROR_STOP=1 --dbname=store --username=zhenya <<-EOSQL
    CREATE TABLE IF NOT EXISTS store_user (
        id                  serial primary key,
        email               varchar(254),
        avatar_url          varchar(254),
        avatar_key          varchar(64),
        shipping_adress     varchar(64),
        credits             integer DEFAULT 0,
        password            varchar(32),
        role                varchar(32)
    );

    CREATE TABLE IF NOT EXISTS store_category (
        id                  serial primary key,
        name                varchar(64)
    );

    CREATE TABLE IF NOT EXISTS store_item (
        id                  serial primary key,
        name                varchar(64),
        value               integer DEFAULT 0,
        quantity            integer DEFAULT 0,
        category_id         integer REFERENCES store_category (id),
        description         varchar(1024)
    );

EOSQL