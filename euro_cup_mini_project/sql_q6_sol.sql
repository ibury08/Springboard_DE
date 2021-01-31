-- Write a SQL query to find the number of matches that were won by a single point, but
-- do not include matches decided by penalty shootout. 
--(misunderstood question, should be where goal_score=1)

 select count( distinct match_no) as n_matches from match_details where goal_score =1; 