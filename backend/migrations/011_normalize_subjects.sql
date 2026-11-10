USE studybuddy;

CREATE TABLE IF NOT EXISTS branch_subjects (
  branch_id INT UNSIGNED NOT NULL,
  subject_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (branch_id, subject_id),
  INDEX ix_branch_subject_subject (subject_id),
  CONSTRAINT fk_bs_branch FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
  CONSTRAINT fk_bs_subject FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO branch_subjects (branch_id, subject_id)
SELECT legacy.branch_id, canonical.id
FROM subjects legacy
JOIN subjects canonical
  ON canonical.code = legacy.code
 AND canonical.branch_id IS NULL
WHERE legacy.branch_id IS NOT NULL
  AND legacy.created_by IS NULL;

INSERT IGNORE INTO user_subjects (user_id, subject_id)
SELECT us.user_id, canonical.id
FROM user_subjects us
JOIN subjects legacy ON legacy.id = us.subject_id AND legacy.branch_id IS NOT NULL
JOIN subjects canonical ON canonical.code = legacy.code AND canonical.branch_id IS NULL;

DELETE us
FROM user_subjects us
JOIN subjects legacy ON legacy.id = us.subject_id
WHERE legacy.branch_id IS NOT NULL AND legacy.created_by IS NULL;

DELETE legacy
FROM subjects legacy
WHERE legacy.branch_id IS NOT NULL
  AND legacy.created_by IS NULL
  AND NOT EXISTS (SELECT 1 FROM games g WHERE g.subject_id = legacy.id);
