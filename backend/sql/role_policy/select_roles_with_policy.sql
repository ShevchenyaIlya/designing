SELECT *
FROM role_policy
INNER JOIN role
    ON (role_policy.role_id=role.id)
WHERE policy_id=%s;
