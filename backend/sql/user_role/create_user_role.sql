CREATE TABLE IF NOT EXISTS user_role(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    role_id BIGSERIAL REFERENCES role(id),
    user_id BIGSERIAL REFERENCES "user"(id)
);