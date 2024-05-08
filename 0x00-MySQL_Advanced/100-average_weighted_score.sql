-- Create a stored procedure to compute and store the average weighted score for a student
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN t_user_id INT)
BEGIN
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE weighted_sum DECIMAL(10, 2);

    -- Calculate total weight and weighted sum
    SELECT SUM(weight) INTO total_weight
    FROM scores
    WHERE user_id = t_user_id;

    SELECT SUM(score * weight) INTO weighted_sum
    FROM scores
    WHERE user_id = t_user_id;

    -- Calculate average weighted score
    INSERT INTO user_weighted_scores (user_id, average_weighted_score)
    VALUES (t_user_id, weighted_sum / total_weight)
    ON DUPLICATE KEY UPDATE average_weighted_score = weighted_sum / total_weight;
END $$

DELIMITER ;
