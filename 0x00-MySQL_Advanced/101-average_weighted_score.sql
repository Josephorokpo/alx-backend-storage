-- Create a stored procedure to compute and store the average weighted score for all students
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE weighted_sum DECIMAL(10, 2);

    -- Calculate total weight and weighted sum
    SELECT SUM(weight) INTO total_weight
    FROM scores;

    SELECT SUM(score * weight) INTO weighted_sum
    FROM scores;

    -- Calculate average weighted score
    INSERT INTO user_weighted_scores (user_id, average_weighted_score)
    SELECT user_id, weighted_sum / total_weight
    FROM scores
    GROUP BY user_id
    ON DUPLICATE KEY UPDATE average_weighted_score = VALUES(average_weighted_score);
END $$

DELIMITER ;
