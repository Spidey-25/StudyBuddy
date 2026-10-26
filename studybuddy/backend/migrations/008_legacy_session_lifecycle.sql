USE studybuddy;

ALTER TABLE study_sessions
  ADD COLUMN client_session_id VARCHAR(64) NULL,
  ADD COLUMN status VARCHAR(16) NOT NULL DEFAULT 'completed',
  ADD COLUMN xp_awarded INT UNSIGNED NOT NULL DEFAULT 0,
  ADD UNIQUE INDEX uq_study_client_session (user_id, client_session_id);

-- Existing legacy rows were saved only after a game was finished.
UPDATE study_sessions SET status='completed' WHERE status IS NULL OR status='';
