SELECT *
FROM unit
INNER JOIN department ON (unit.department_id=department.id)
INNER JOIN "user" ON ("user".id=unit.head_id)
WHERE department_id=%s;
