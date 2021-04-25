UPDATE policy
SET
    title=COALESCE(%s, title),
    description=COALESCE(%s, description),
    is_administrative=COALESCE(%s, is_administrative)
WHERE id=%s;