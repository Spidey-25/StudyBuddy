USE studybuddy;

-- Additive platform-session store; existing local study_sessions data is preserved.
CREATE TABLE IF NOT EXISTS platform_game_sessions (
    id CHAR(36) PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    game_id VARCHAR(80) NOT NULL,
    subject_code VARCHAR(60) NOT NULL,
    state_json JSON NOT NULL,
    score INT UNSIGNED NOT NULL DEFAULT 0,
    mistakes INT UNSIGNED NOT NULL DEFAULT 0,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    seconds INT UNSIGNED NOT NULL DEFAULT 0,
    INDEX ix_platform_user_subject (user_id, subject_code),
    INDEX ix_platform_game (game_id),
    CONSTRAINT fk_platform_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
