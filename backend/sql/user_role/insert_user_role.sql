INSERT INTO user_role(
    role_id,
    role_id
) VALUES (%s, %s)
RETURNING id;