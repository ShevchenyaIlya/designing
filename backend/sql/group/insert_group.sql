INSERT INTO group(
    name,
    description
) VALUES (%s, %s)
RETURNING id;