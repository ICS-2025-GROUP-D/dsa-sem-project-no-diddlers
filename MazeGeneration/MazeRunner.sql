CREATE DATABASE IF NOT EXISTS maze_runner_db;
USE maze_runner_db;

-- Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- LeaderBoard table (redundant)
CREATE TABLE IF NOT EXISTS LeaderBoard (
    leaderboard_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    score INT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

-- Index for ranking
CREATE INDEX idx_leaderboard_score ON LeaderBoard(score DESC);

-- Trigger to auto-update LeaderBoard when Users.score changes
DELIMITER //
CREATE TRIGGER update_leaderboard
AFTER UPDATE ON Users
FOR EACH ROW
BEGIN
    INSERT INTO LeaderBoard (username, score)
    VALUES (NEW.username, NEW.score)
    ON DUPLICATE KEY UPDATE score = NEW.score;
END //
DELIMITER ;