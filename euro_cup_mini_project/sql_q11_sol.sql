-- Write a SQL query to find the players, their jersey number, and playing club who
-- were the goalkeepers for England in EURO Cup 2016

select player_id, player_name, jersey_no, playing_club from player_mast where posi_to_play = 'GK' and team_id in (select country_id from soccer_country where country_name = 'England');
