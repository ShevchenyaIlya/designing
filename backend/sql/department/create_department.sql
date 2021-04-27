CREATE TABLE IF NOT EXISTS department(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    head_id BIGSERIAL
);