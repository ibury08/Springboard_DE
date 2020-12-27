-- 14. Write a SQL query to find referees and the number of bookings they made for the
-- entire tournament. Sort your answer by the number of bookings in descending order.
select referee_name, sum(n_bookings) as bookings from (
select match_no, count(*) as n_bookings from player_booked group by match_no) P
join (select match_no, referee_id from match_mast) M using (match_no)
join referee_mast using (referee_id)
group by referee_name order by bookings desc;
