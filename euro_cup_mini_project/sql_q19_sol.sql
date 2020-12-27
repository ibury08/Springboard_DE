-- 19. Write a SQL query to find the number of captains who were also goalkeepers.
select count(*) as n_captains from
(select * from player_mast where posi_to_play = 'GK') P
join (select distinct player_captain from match_captain) C
on P.player_id = C.player_captain;
