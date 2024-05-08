-- Create a stored procedure to compute and store the average score for a user
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN t_user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Calculate average score
    SELECT AVG(score) INTO avg_score
    FROM scores
    WHERE user_id = t_user_id;

    -- Update or insert the average score
    INSERT INTO user_scores (user_id, average_score)
    VALUES (t_user_id, avg_score)
    ON DUPLICATE KEY UPDATE average_score = avg_score;
END $$

DELIMITER ;
