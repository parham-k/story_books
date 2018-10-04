#!/usr/bin/env bash

apt install postgresql
su postgres -c "psql < init_psql.sql"
