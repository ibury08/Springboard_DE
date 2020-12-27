-- Write a SQL query to find all the venues where matches with penalty shootouts were
-- played.



select * from soccer_venue where venue_id in (select venue_id from match_mast where decided_by = 'P');
