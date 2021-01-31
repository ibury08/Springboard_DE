-- 13. Write a SQL query to find all the defenders who scored a goal for their teams.

select distinct player_name from goal_details 
join player_mast using (player_id)
join playing_position on player_mast.posi_to_play = playing_position.position_id
where position_desc = 'Defenders';