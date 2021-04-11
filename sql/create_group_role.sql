CREATE TABLE IF NOT EXISTS group_role(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    group_id BIGSERIAL REFERENCES "group"(group_id),
    role_id BIGSERIAL REFERENCES role(role_id)
);