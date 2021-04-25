CREATE TABLE IF NOT EXISTS unit(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    department_id BIGSERIAL REFERENCES department(id),
    head_id BIGSERIAL
);