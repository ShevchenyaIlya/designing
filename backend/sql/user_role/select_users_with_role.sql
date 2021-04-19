SELECT *
FROM user_role
INNER JOIN "user"
    ON (user_role.user_id="user".id)
INNER JOIN role
    ON (user_role.role_id=role.id)
WHERE role_id=%s;
