SELECT *
FROM group_role
INNER JOIN "group"
    ON (group_role.group_id="group".id)
INNER JOIN role
    ON (group_role.role_id=role.id)
WHERE group_id=%s;
