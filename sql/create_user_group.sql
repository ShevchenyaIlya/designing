CREATE TABLE IF NOT EXISTS user_group(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    group_id BIGSERIAL REFERENCES "group"(group_id),
    user_id BIGSERIAL REFERENCES "user"(user_id)
);