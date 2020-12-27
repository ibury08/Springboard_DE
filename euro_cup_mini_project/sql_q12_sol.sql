-- Write a SQL query that returns the total number of goals scored by each position on
-- each country’s team. Do not include positions which scored no goals

select country_name, posi_to_play as position, count(*) as n_goals  from 
(select player_id from goal_details) G 
join (select player_id, team_id, posi_to_play from player_mast ) P 
on G.player_id = P.player_id
join (select country_id, country_name from soccer_country) C
on P.team_id = C.country_id
group by country_name, position;
