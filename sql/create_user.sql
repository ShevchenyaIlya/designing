CREATE TABLE IF NOT EXISTS user(
    user_id BIGSERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    middle_name VARCHAR(200),
    register_date DATE,
    email VARCHAR(200),
    password VARCHAR(256),
    near_manager_id BIGSERIAL REFERENCES user(user_id),
    department_id BIGSERIAL REFERENCES department(department_id),
    unit_id BIGSERIAL REFERENCES unit(unit_id),
    position_id BIGSERIAL REFERENCES position(position_id)
);