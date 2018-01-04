#!/usr/bin/env bash

PGPASSWORD=zhenya psql -v ON_ERROR_STOP=1 --dbname=store --username=zhenya <<-EOSQL
    CREATE TABLE IF NOT EXISTS store_user (
        id                  serial primary key,
        email               varchar(254),
        avatar              varchar(64),
        shipping_adress     varchar(64),
        credits             integer DEFAULT 0,
        password            varchar(32),
        role                varchar(32)
    );
EOSQL