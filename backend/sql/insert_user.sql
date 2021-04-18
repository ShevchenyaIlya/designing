INSERT INTO "user"(
      first_name,
      last_name,
      middle_name,
      email,
      password,
      register_date,
      department_id,
      unit_id,
      position_id
)
VALUES (%s, %s, %s, %s, %s, null, null, null, null)
RETURNING user_id;