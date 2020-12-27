-- Write a SQL query to find the number of matches that were won by a single point, but
-- do not include matches decided by penalty shootout.
with goals as (

select abs( left(goal_score, position('-' in goal_score)-1) - right(goal_score,position('-' in goal_score)-1)) as goal_diff from match_mast where decided_by != 'P' )

select count(*) as n_matches from goals where goal_diff = 1;
