-- Persist one server-validated record per platform game action for timing,
-- weak-game and question-quality analytics. Cascades only with its owner/session.
CREATE TABLE IF NOT EXISTS platform_game_attempts (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  platform_session_id CHAR(36) NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  game_id VARCHAR(80) NOT NULL,
  subject_code VARCHAR(60) NOT NULL,
  level_index INT UNSIGNED NOT NULL,
  topic VARCHAR(160) NOT NULL,
  objective VARCHAR(500) NOT NULL,
  correct BOOLEAN NOT NULL,
  response_seconds INT UNSIGNED NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_platform_attempt_topic (subject_code, game_id, correct),
  CONSTRAINT fk_platform_attempt_session FOREIGN KEY (platform_session_id)
    REFERENCES platform_game_sessions(id) ON DELETE CASCADE,
  CONSTRAINT fk_platform_attempt_user FOREIGN KEY (user_id)
    REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
