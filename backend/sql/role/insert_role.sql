INSERT INTO role(
    name,
    description
) VALUES (%s, %s)
RETURNING id;