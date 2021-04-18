INSERT INTO unit(
    name,
    description,
    department_id,
    head_id
) VALUES (%s, %s, %s, %s)
RETURNING id;