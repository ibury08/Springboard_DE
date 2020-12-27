-- Write a SQL query to find the country where the most assistant referees come from,
-- and the count of the assistant referees.
select country_name, n_refs from 
(select country_id, count(*) as n_refs from asst_referee_mast group by country_id) A 
join soccer_country using (country_id);
