-- 18. Write a SQL query to find the highest number of foul cards given in one match.
select match_no, count(*) as n_cards from player_booked group by match_no order by n_cards desc limit 1;
