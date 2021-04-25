INSERT INTO user_group(
    group_id,
    user_id
) VALUES (%s, %s)
RETURNING id;