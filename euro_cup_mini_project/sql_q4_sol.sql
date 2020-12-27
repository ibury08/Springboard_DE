-- Write a SQL query to compute a list showing the number of substitutions that
-- happened in various stages of play for the entire tournament.
select play_stage, count(*) as n_subs from
(select match_no from player_in_out where in_out = 'I') A join (select match_no, play_stage from match_mast) B
using (match_no) group by play_stage ;
