CREATE TABLE IF NOT EXISTS role_policy(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    role_id BIGSERIAL REFERENCES role(id),
    policy_id BIGSERIAL REFERENCES policy(id),
    department_id BIGSERIAL REFERENCES department(id),
    target_user_id BIGSERIAL REFERENCES "user"(id)
);