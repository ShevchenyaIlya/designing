SELECT *
FROM role_policy
INNER JOIN policy
    ON (role_policy.policy_id=policy.id)
INNER JOIN role
    ON (role_policy.role_id=role.id)
INNER JOIN department
    ON (role_policy.department_id=department.id)
WHERE role_id=%s;
