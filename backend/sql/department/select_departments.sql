SELECT *
FROM department
INNER JOIN "user"
ON (department.head_id="user".id);
