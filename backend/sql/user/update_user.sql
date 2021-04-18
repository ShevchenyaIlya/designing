UPDATE "user"
SET
    first_name=COALESCE(%s, first_name),
    last_name=COALESCE(%s, last_name),
    middle_name=COALESCE(%s, middle_name),
    department_id=COALESCE(%s, department_id),
    unit_id=COALESCE(%s, unit_id),
    position_id=COALESCE(%s, position_id)
WHERE email=%s;