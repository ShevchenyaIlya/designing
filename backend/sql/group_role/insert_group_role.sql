INSERT INTO group_role(
    group_id,
    role_id
) VALUES (%s, %s)
RETURNING id;