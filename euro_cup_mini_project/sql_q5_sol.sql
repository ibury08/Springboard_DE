-- Write a SQL query to find the number of bookings that happened in stoppage time.
select count(*) as n_bookings from player_booked where play_schedule = 'ST';
