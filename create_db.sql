-- Create the user_account table
CREATE TABLE user_account (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

-- Create the job_title table
CREATE TABLE job_title (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL
);

-- Create the skill_category table
CREATE TABLE skill_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    job_title_id INTEGER REFERENCES job_title(id) ON DELETE CASCADE
);

-- Create the skill table
CREATE TABLE skill (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

-- Create the skill_category_skill table
CREATE TABLE skill_category_skill (
    skill_category_id INTEGER REFERENCES skill_category(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skill(id) ON DELETE CASCADE,
    PRIMARY KEY (skill_category_id, skill_id)
);

-- Create the user_skill table
CREATE TABLE user_skill (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_account(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skill(id) ON DELETE CASCADE,
    level VARCHAR(64) NOT NULL,
    UNIQUE (user_id, skill_id)
);


-- Insert job titles
INSERT INTO job_title (name) VALUES ('Software Engineer');
INSERT INTO job_title (name) VALUES ('Data Scientist');

-- Insert skills
INSERT INTO skill (name) VALUES ('Python');
INSERT INTO skill (name) VALUES ('Java');
INSERT INTO skill (name) VALUES ('SQL');

-- Insert users
INSERT INTO user_account (username, email) VALUES ('john_doe', 'john@example.com');
INSERT INTO user_account (username, email) VALUES ('jane_smith', 'jane@example.com');

-- Insert skill categories
INSERT INTO skill_category (name, job_title_id) VALUES ('Programming Languages', 1);
INSERT INTO skill_category (name, job_title_id) VALUES ('Data Analysis', 2);

-- Associate skills with skill categories
INSERT INTO skill_category_skill (skill_category_id, skill_id) VALUES (1, 1);  -- Programming Languages -> Python
INSERT INTO skill_category_skill (skill_category_id, skill_id) VALUES (1, 2);  -- Programming Languages -> Java
INSERT INTO skill_category_skill (skill_category_id, skill_id) VALUES (2, 3);  -- Data Analysis -> SQL

-- Associate users with skills
INSERT INTO user_skill (user_id, skill_id, level) VALUES (1, 1, 'Advanced');  -- john_doe -> Python
INSERT INTO user_skill (user_id, skill_id, level) VALUES (1, 3, 'Intermediate');  -- john_doe -> SQL
INSERT INTO user_skill (user_id, skill_id, level) VALUES (2, 2, 'Beginner');  -- jane_smith -> Java
INSERT INTO user_skill (user_id, skill_id, level) VALUES (2, 3, 'Advanced');  -- jane_smith -> SQL
