SELECT "user".first_name,
       "user".last_name,
       "user".middle_name,
       "user".email,
       department.name as department_name,
       department.description as department_description,
       unit.*
FROM unit
INNER JOIN department ON (unit.department_id=department.id)
INNER JOIN "user" ON ("user".id=unit.head_id)
WHERE unit.department_id=%s;
