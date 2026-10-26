USE studybuddy;

ALTER TABLE platform_game_attempts
  ADD COLUMN client_action_id CHAR(36) NULL,
  ADD COLUMN response_json JSON NULL,
  ADD UNIQUE INDEX uq_platform_action_id (platform_session_id, client_action_id);
