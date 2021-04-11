CREATE TABLE IF NOT EXISTS user_role(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    role_id BIGSERIAL REFERENCES role(role_id),
    user_id BIGSERIAL REFERENCES user(user_id)
);