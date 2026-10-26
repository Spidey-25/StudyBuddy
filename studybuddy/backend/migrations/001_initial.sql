CREATE DATABASE IF NOT EXISTS studybuddy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE studybuddy;

-- The executable Flask startup applies the same schema through ensure_schema().
-- Keep this migration as a reviewable deployment artifact.
CREATE TABLE IF NOT EXISTS branches (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, code VARCHAR(40) NOT NULL UNIQUE, name VARCHAR(120) NOT NULL);
CREATE TABLE IF NOT EXISTS users (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, email VARCHAR(190) NOT NULL UNIQUE, username VARCHAR(40) NOT NULL, password_hash VARCHAR(255) NOT NULL, display_name VARCHAR(40) NOT NULL, role ENUM('student','teacher') NOT NULL DEFAULT 'student', branch_id INT UNSIGNED NULL, course VARCHAR(120) NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS subjects (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, code VARCHAR(60) NOT NULL, name VARCHAR(160) NOT NULL, branch_id INT UNSIGNED NULL, created_by INT UNSIGNED NULL, UNIQUE KEY uq_subject_branch (code, branch_id));
CREATE TABLE IF NOT EXISTS user_subjects (user_id INT UNSIGNED NOT NULL, subject_id INT UNSIGNED NOT NULL, PRIMARY KEY (user_id, subject_id));
CREATE TABLE IF NOT EXISTS games (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, subject_id INT UNSIGNED NOT NULL, title VARCHAR(160) NOT NULL, game_type VARCHAR(40) NOT NULL, content_json JSON NOT NULL, UNIQUE KEY uq_game_subject_title (subject_id, title));
