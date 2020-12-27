-- Write a SQL query to find the match number for the game with the highest number of
-- penalty shots, and which countries played that match


with m as (
select match_no, count(*) as n_shots from penalty_shootout group by match_no order by n_shots desc limit 1) 


select match_no, country_name from penalty_shootout  inner join m using(match_no) inner join soccer_team using(team_id) inner join soccer_country on soccer_team.team_id = soccer_country.country_id group by match_no, country_name;

