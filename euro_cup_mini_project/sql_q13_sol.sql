-- 13. Write a SQL query to find all the defenders who scored a goal for their teams.
with def as
(select * from player_mast where posi_to_play 
	in (select position_id from playing_position where position_desc = 'Defenders'))
select def.* from goal_details join def using (player_id);
