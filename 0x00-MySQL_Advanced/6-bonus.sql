-- Script that creates a stored procedure AddBonus
-- that adds a new correction for a student.
DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN t_user_id INT,
    IN t_project_name VARCHAR(255),
    IN t_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if project exists, create if not
    INSERT INTO projects (name)
    SELECT t_project_name
    WHERE t_project_name NOT IN (SELECT name FROM projects);

    -- Get project ID
    SET project_id = (SELECT id FROM projects WHERE name = t_project_name);

    -- Insert correction
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (t_user_id, project_id, t_score);
END $$

DELIMITER ;
