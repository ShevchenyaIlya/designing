INSERT INTO position(
    title,
    level
) VALUES (%s, %s)
RETURNING id;