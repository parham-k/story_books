CREATE DATABASE story_books_db;
CREATE USER story_books_user WITH PASSWORD 'St0ryB00k$';
ALTER ROLE story_books_user SET client_encoding TO 'utf8';
ALTER ROLE story_books_user SET timezone TO 'UTC';
ALTER ROLE story_books_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE story_books_db TO story_books_user;
ALTER USER story_books_user CREATEDB;