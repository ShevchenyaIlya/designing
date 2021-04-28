SELECT policy.*
FROM user_group
INNER JOIN "group"
    ON (user_group.group_id="group".id)
INNER JOIN group_role
    ON (group_role.group_id=user_group.group_id)
INNER JOIN role
    ON (role.id=group_role.role_id)
INNER JOIN role_policy
    ON (role_policy.role_id=role.id)
INNER JOIN policy
    ON (policy.id=role_policy.policy_id)
WHERE user_id=%s
UNION
SELECT policy.*
FROM user_role
INNER JOIN role
    ON (role.id=user_role.role_id)
INNER JOIN role_policy
    ON (role_policy.role_id=role.id)
INNER JOIN policy
    ON (policy.id=role_policy.policy_id)
WHERE user_id=%s;

