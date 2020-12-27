-- 15. Write a SQL query to find the referees who booked the most number of players
select referee_name, count(distinct player_id) as players_booked from (
select match_no, player_id  from player_booked ) P
join (select match_no, referee_id from match_mast) M using (match_no)
join referee_mast using (referee_id)
group by referee_name order by players_booked desc limit 5;
