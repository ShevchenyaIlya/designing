DELETE FROM role_policy
WHERE role_id=%s AND policy_id=%s AND department_id=%s AND target_user_id=%s;