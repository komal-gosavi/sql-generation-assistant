CREATE ROLE sql_assistant_app
LOGIN
PASSWORD 'readonly_password';

GRANT CONNECT ON DATABASE sql_assistant TO sql_assistant_app;

GRANT USAGE ON SCHEMA public TO sql_assistant_app;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO sql_assistant_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO sql_assistant_app;