INSERT INTO user_role(
    user_id,
    role_id
) VALUES (%s, %s)
RETURNING id;