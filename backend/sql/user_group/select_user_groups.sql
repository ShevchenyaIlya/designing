SELECT *
FROM user_group
INNER JOIN "group"
    ON (user_group.group_id="group".id)
INNER JOIN "user"
    ON (user_group.user_id="user".id)
WHERE user_id=%s;
