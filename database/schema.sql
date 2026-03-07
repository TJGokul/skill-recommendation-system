-- Create database
CREATE DATABASE IF NOT EXISTS skill_recommendation_db;

-- Use the database
USE skill_recommendation_db;

-- Create tables (Django will create these automatically with migrations)
-- But here's the schema for reference

-- Skills table
CREATE TABLE IF NOT EXISTS api_skill (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT
);

-- Jobs table
CREATE TABLE IF NOT EXISTS api_job (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT NOT NULL,
    location VARCHAR(100) NOT NULL,
    salary_min INTEGER,
    salary_max INTEGER,
    employment_type VARCHAR(50) NOT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO api_skill (name, category) VALUES
('Python', 'programming'),
('JavaScript', 'programming'),
('Java', 'programming'),
('React', 'frameworks'),
('Django', 'frameworks'),
('SQL', 'databases'),
('AWS', 'cloud'),
('Docker', 'cloud'),
('Communication', 'soft_skills'),
('Leadership', 'soft_skills');

INSERT INTO api_job (title, company, description, requirements, location, salary_min, salary_max, employment_type) VALUES
('Senior Python Developer', 'Tech Corp', 'Looking for an experienced Python developer...', '5+ years Python experience, Django, REST APIs', 'San Francisco, CA', 120, 180, 'full-time'),
('Full Stack Engineer', 'Startup Inc', 'Join our dynamic team building modern web apps...', 'React, Node.js, MongoDB', 'New York, NY', 100, 150, 'full-time'),
('Data Scientist', 'AI Solutions', 'Apply machine learning to solve complex problems...', 'Python, TensorFlow, SQL, Statistics', 'Boston, MA', 130, 190, 'full-time'),
('DevOps Engineer', 'Cloud Systems', 'Manage and scale cloud infrastructure...', 'AWS, Docker, Kubernetes, CI/CD', 'Remote', 110, 160, 'remote'),
('Frontend Developer', 'Design Studio', 'Create beautiful and responsive user interfaces...', 'React, TypeScript, CSS', 'Austin, TX', 90, 130, 'full-time');