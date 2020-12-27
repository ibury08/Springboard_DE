-- 20. Write a SQL query to find the substitute players who came into the field in the first
-- half of play, within a normal play schedule.

select player_id, jersey_no, player_name, posi_to_play from (
select player_id from player_in_out where play_schedule = 'NT' and in_out = 'I' and play_half = 1) s 
join player_mast using (player_id);
