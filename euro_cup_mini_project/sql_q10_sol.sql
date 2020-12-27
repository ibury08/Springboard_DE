-- Write a SQL query to find all available information about the players under contract to
-- Liverpool F.C. playing for England in EURO Cup 2016.
select P.* from (select * from player_mast where playing_club='Liverpool')P join (select * from soccer_country where country_name = 'England') B on P.team_id = B.country_id;
