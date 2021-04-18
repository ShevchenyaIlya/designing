UPDATE department
SET
    name=COALESCE(%s, name),
    description=COALESCE(%s, description),
    head_id=COALESCE(%s, head_id)
WHERE id=%s;