CREATE TABLE IF NOT EXISTS department(
    department_id BIGSERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    head_id BIGSERIAL
);