CREATE TABLE IF NOT EXISTS role_policy(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    role_id BIGSERIAL REFERENCES role(role_id),
    policy_id BIGSERIAL REFERENCES policy(policy_id),
    department_id BIGSERIAL REFERENCES department(department_id),
    target_user_id BIGSERIAL REFERENCES "user"(user_id)
);