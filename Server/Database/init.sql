
CREATE DATABASE student_log;
USE student_log;
CREATE TABLE students(
    "id" INT(10) PRIMARY KEY NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL
);
CREATE TABLE classes(
    "id" INT(10) PRIMARY KEY AUTO_INCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "teacher" VARCHAR(255) NOT NULL
);
CREATE TABLE students_out(
    "id" INT(10) PRIMARY KEY AUTO_INCREMENT NOT NULL,
    "student_id" INT(10) NOT NULL,
    "class_id" INT(10) NOT NULL,
    "time_out" DATE NOT NULL,
    "destination" VARCHAR(255) NOT NULL
);
CREATE TABLE log(
    "id" INT(10) PRIMARY KEY AUTO_INCREMENT NOT NULL,
    "student_id" INT(10) NOT NULL,
    "class_id" INT(10) NOT NULL,
    "time_out" DATE NOT NULL,
    "time_in" DATE NOT NULL,
    "destination" VARCHAR(255) NOT NULL
);
CREATE TABLE users(
    "id" INT PRIMARY KEY AUTO_INCREMENT,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL
);
