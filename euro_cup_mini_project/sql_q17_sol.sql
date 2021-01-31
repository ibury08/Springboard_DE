-- Write a SQL query to find the country where the most assistant referees come from,
-- and the count of the assistant referees.
select country_name, count(*) as n_refs from asst_referee_mast
join soccer_country using (country_id)
group by country_name order by n_refs desc limit 1;