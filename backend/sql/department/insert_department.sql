INSERT INTO department(
    name,
    description,
    head_id
) VALUES (%s, %s, %s)
RETURNING id;