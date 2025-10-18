-- Database initialization script for Restaurant Seating System
-- This script is run when the MariaDB container starts

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS restaurant_seating;

-- Use the database
USE restaurant_seating;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON restaurant_seating.* TO 'restaurant_user'@'%';
FLUSH PRIVILEGES;
