CREATE TABLE IF NOT EXISTS policy(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    is_administrative BOOLEAN
);