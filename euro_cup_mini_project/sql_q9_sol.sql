-- Write a SQL query to find the goalkeeper’s name and jersey number, playing for
-- Germany, who played in Germany’s group stage matches.


with gk as (
select player_gk from match_details where team_id in (select country_id from soccer_country where country_name = 'Germany') and play_stage = 'G')

select distinct player_name, jersey_no from player_mast join gk on player_mast.player_id = gk.player_gk
;
