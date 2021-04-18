UPDATE position
SET
    title=COALESCE(%s, title),
    level=COALESCE(%s, level)
WHERE id=%s;