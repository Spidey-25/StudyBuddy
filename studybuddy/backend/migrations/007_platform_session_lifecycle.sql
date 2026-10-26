USE studybuddy;

-- Additive lifecycle and reward fields for platform game sessions.
ALTER TABLE platform_game_sessions
  ADD COLUMN accuracy DECIMAL(5,2) NOT NULL DEFAULT 0,
  ADD COLUMN xp_awarded INT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN status VARCHAR(16) NOT NULL DEFAULT 'active',
  ADD COLUMN ended_at TIMESTAMP NULL,
  ADD INDEX ix_platform_status_user (user_id, status);

-- Preserve old completion records and make them terminal after the upgrade.
UPDATE platform_game_sessions
SET status='completed', ended_at=COALESCE(ended_at, completed_at)
WHERE completed_at IS NOT NULL;
