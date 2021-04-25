SELECT "user".first_name, "user".last_name, "user".middle_name, "user".email, department.*
FROM department
INNER JOIN "user"
ON (department.head_id="user".id)
WHERE department.id=%s;