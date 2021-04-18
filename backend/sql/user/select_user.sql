SELECT *
FROM "user"
LEFT JOIN position
    ON ("user".position_id=position.position_id)
WHERE email=%s;