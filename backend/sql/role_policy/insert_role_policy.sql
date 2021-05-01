INSERT INTO role_policy(
    role_id,
    policy_id,
    department_id
) VALUES (%s, %s, %s)
RETURNING id;