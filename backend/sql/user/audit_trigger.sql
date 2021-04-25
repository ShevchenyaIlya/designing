CREATE OR REPLACE FUNCTION process_user_audit() RETURNS TRIGGER AS $user_audit$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO user_audit SELECT 'DELETE', now(), OLD.*;
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO user_audit SELECT 'UPDATE', now(), NEW.*;
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO user_audit SELECT 'INSERT', now(), NEW.*;
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$user_audit$ LANGUAGE plpgsql;

CREATE TRIGGER user_audit
AFTER INSERT OR UPDATE OR DELETE ON "user"
    FOR EACH ROW EXECUTE PROCEDURE process_user_audit();