SELECT "user".first_name,
       "user".last_name,
       "user".middle_name,
       "user".email,
       department.name as department_name,
       department.description as department_description,
       unit.*
FROM unit
WHERE id=%s;