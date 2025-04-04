CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
	current_topic integer DEFAULT 1,
    current_stage integer DEFAULT 1,
    is_audio_enabled BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE conversation_history (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role VARCHAR(10) CHECK (role IN ('user', 'system')),
    message TEXT NOT NULL,
	current_topic INT NOT NULL,
    current_stage INT NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	-- Cascading deletion where if a user is deleted, all its conversation history will be cleared as well
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);