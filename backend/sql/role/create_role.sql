CREATE TABLE IF NOT EXISTS role(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);