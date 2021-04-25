INSERT INTO policy(
    title,
    description,
    is_administrative
) VALUES (%s, %s, %s)
RETURNING id;