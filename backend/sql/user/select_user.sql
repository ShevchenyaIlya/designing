SELECT *
FROM "user"
LEFT JOIN position
    ON ("user".position_id=position.id)
WHERE email=%s;