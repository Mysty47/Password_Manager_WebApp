-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS login_info;

-- Use the database
USE login_info;

-- Create the webappdb table if it doesn't exist
CREATE TABLE IF NOT EXISTS webappdb (
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create the saved_passwords table if it doesn't exist
CREATE TABLE IF NOT EXISTS saved_passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
); 