-- 16. Write a SQL query to find referees and the number of matches they worked in each
-- venue.
select referee_name, venue_id,count(*) as n_games from
(select venue_id, referee_id from match_mast) M
join referee_mast using (referee_id) group by referee_name, venue_id;
