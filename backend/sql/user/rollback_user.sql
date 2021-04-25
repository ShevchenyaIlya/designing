CREATE OR REPLACE FUNCTION rollback_changes(rollback_time TIMESTAMP)
RETURNS VOID
AS $$
DECLARE
   t_row user_audit%rowtype;
BEGIN
    FOR t_row in SELECT * FROM user_audit WHERE action_time>=rollback_time ORDER BY action_time DESC
    LOOP
        raise notice 'Value: %, %, %', t_row.operation, t_row.action_time, t_row.user_id;
        IF (t_row.operation = 'DELETE') THEN
            INSERT INTO "user" SELECT t_row.user_id, t_row.first_name, t_row.last_name, t_row.middle_name, t_row.register_date, t_row.email, t_row.password, t_row.near_manager_id, t_row.department_id, t_row.unit_id, t_row.position_id;
        ELSIF (t_row.operation = 'UPDATE') THEN
            UPDATE "user" SET first_name=t_row.first_name, last_name=t_row.last_name, middle_name=t_row.middle_name, register_date=t_row.register_date, email=t_row.email, password=t_row.password, near_manager_id=t_row.near_manager_id, department_id=t_row.department_id, unit_id=t_row.unit_id, position_id=t_row.position_id WHERE id=t_row.user_id;
        ELSIF (t_row.operation = 'INSERT') THEN
            DELETE FROM "user" WHERE id=t_row.user_id;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
