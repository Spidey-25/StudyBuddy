-- Add the current computing-focused branch and subject catalog additively.
-- Existing rows and user selections are preserved; the application filters
-- retired legacy school-subject codes out of the active catalog.
INSERT IGNORE INTO branches (code, name) VALUES
('cse', 'Computer Science and Engineering'),
('it', 'Information Technology'),
('ce', 'Computer Engineering'),
('aiml', 'Artificial Intelligence and Machine Learning'),
('ds', 'Data Science'),
('cyber', 'Cybersecurity');

INSERT IGNORE INTO subjects (code, name, branch_id)
SELECT catalog.code, catalog.name, b.id
FROM branches b
JOIN (
  SELECT 'C' code, 'C Programming' name UNION ALL
  SELECT 'CPP', 'C++' UNION ALL
  SELECT 'JAVA', 'Java' UNION ALL
  SELECT 'PYTHON', 'Python' UNION ALL
  SELECT 'DSA', 'Data Structures and Algorithms' UNION ALL
  SELECT 'DBMS', 'Database Management Systems' UNION ALL
  SELECT 'OS', 'Operating Systems' UNION ALL
  SELECT 'CN', 'Computer Networks' UNION ALL
  SELECT 'WEB', 'Web Development' UNION ALL
  SELECT 'SE', 'Software Engineering' UNION ALL
  SELECT 'AI', 'Artificial Intelligence' UNION ALL
  SELECT 'ML', 'Machine Learning' UNION ALL
  SELECT 'CYBER', 'Cybersecurity' UNION ALL
  SELECT 'CLOUD', 'Cloud Computing' UNION ALL
  SELECT 'EMBEDDED', 'Embedded Systems' UNION ALL
  SELECT 'IOT', 'Internet of Things'
) catalog ON (
  b.code = 'cse'
  OR (b.code = 'it' AND catalog.code NOT IN ('AI', 'ML', 'EMBEDDED', 'IOT'))
  OR (b.code = 'ce' AND catalog.code IN ('C','CPP','JAVA','PYTHON','DSA','DBMS','OS','CN','EMBEDDED','IOT'))
  OR (b.code = 'aiml' AND catalog.code IN ('JAVA','PYTHON','DSA','DBMS','OS','CN','AI','ML','CLOUD'))
  OR (b.code = 'ds' AND catalog.code IN ('JAVA','PYTHON','DSA','DBMS','OS','CN','AI','ML','CLOUD'))
  OR (b.code = 'cyber' AND catalog.code IN ('C','CPP','JAVA','PYTHON','DSA','DBMS','OS','CN','WEB','CYBER','CLOUD'))
);
