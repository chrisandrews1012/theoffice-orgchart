CREATE TABLE IF NOT EXISTS executive (
    emp_id VARCHAR PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    position VARCHAR,
    department VARCHAR,
    supervisor_id VARCHAR DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS manager (
    emp_id VARCHAR PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    position VARCHAR,
    department VARCHAR,
    supervisor_id VARCHAR REFERENCES executive(emp_id) ON DELETE SET NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS employee (
    emp_id VARCHAR PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    position VARCHAR,
    department VARCHAR,
    supervisor_id VARCHAR REFERENCES manager(emp_id) ON DELETE SET NULL DEFAULT NULL
);