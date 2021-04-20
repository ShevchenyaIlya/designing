CREATE TABLE IF NOT EXISTS user_audit(
    operation VARCHAR(20),
    action_time TIMESTAMP,
    user_id BIGINT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    middle_name VARCHAR(200),
    register_date DATE,
    email VARCHAR(200),
    password VARCHAR(256),
    near_manager_id BIGINT,
    department_id BIGINT,
    unit_id BIGINT,
    position_id BIGINT
);