UPDATE role
SET
    name=COALESCE(%s, name),
    description=COALESCE(%s, description)
WHERE id=%s;