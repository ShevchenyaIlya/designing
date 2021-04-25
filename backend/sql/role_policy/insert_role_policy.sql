INSERT INTO role_policy(
    role_id,
    policy_id,
    department_id,
    target_user_id
) VALUES (%s, %s, %s, %s)
RETURNING id;