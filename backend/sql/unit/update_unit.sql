UPDATE unit
SET
    name=COALESCE(%s, name),
    description=COALESCE(%s, description),
    department_id=COALESCE(%s, department_id),
    head_id=COALESCE(%s, head_id)
WHERE id=%s;