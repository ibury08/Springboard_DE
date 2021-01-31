-- Write a SQL query to compute a list showing the number of substitutions that
-- happened in various stages of play for the entire tournament (== play_half, play_schedule).
select play_schedule, play_half, count(*) from player_in_out group by 1, 2;
