--
-- File generated with SQLiteStudio v3.2.1 on Tue Mar 31 20:54:03 2020
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: books
CREATE TABLE books (
    book_id    INTEGER PRIMARY KEY,
    title      TEXT,
    author     TEXT,
    publishing TEXT,
    price      REAL,
    year       INTEGER,
    genre_id   INTEGER REFERENCES genres (genre_id) ON DELETE RESTRICT
                                                    ON UPDATE CASCADE,
    status     TEXT    DEFAULT (0) 
);


-- Table: borrows
CREATE TABLE borrows (
    borrow_id  INTEGER PRIMARY KEY,
    date       DATE    NOT NULL,
    student_id INTEGER NOT NULL
                       REFERENCES students (student_id) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
    book_id    INTEGER NOT NULL
                       REFERENCES books (book_id) ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
    status     INTEGER DEFAULT (0) 
);


-- Table: genres
CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL
);


-- Table: students
CREATE TABLE students (
    student_id    INTEGER PRIMARY KEY,
    first_name    TEXT    NOT NULL,
    last_name     TEXT    NOT NULL,
    class_number  INTEGER NOT NULL,
    class_letter  TEXT    NOT NULL,
    phone         TEXT    NOT NULL,
    email         TEXT,
    parents_phone TEXT,
    adress        TEXT
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
