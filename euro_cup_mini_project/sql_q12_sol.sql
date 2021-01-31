-- Write a SQL query that returns the total number of goals scored by each position on
-- each country’s team. Do not include positions which scored no goals

select country_name, posi_to_play as position, count(*) as n_goals 
from goal_details
join player_mast using (player_id)
join soccer_country on player_mast.team_id = soccer_country.country_id
group by country_name, position; 
