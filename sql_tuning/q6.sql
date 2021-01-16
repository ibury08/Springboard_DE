USE springboardopt;

-- -------------------------------------
SET @v1 = 1612521;
SET @v2 = 1145072;
SET @v3 = 1828467;
SET @v4 = 'MGT382';
SET @v5 = 'Amber Hill';
SET @v6 = 'MGT';
SET @v7 = 'EE';			  
SET @v8 = 'MAT';

-- 6. List the names of students who have taken all courses offered by department v8 (deptId).
SELECT name FROM Student,
	(SELECT studId
	FROM Transcript
		WHERE crsCode IN
		(SELECT crsCode FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))
		GROUP BY studId
		HAVING COUNT(*) = 
			(SELECT COUNT(*) FROM Course WHERE deptId = @v8 AND crsCode IN (SELECT crsCode FROM Teaching))) as alias
WHERE id = alias.studId;

--Optimized query
--*What was the bottleneck?
-- There's no need to reference Teaching. 
--How did you identify it?
-- The IN subquery did not provide a filter clause, thus doing nothing.
-- What method you chose to resolve the bottleneck
-- Removed the Teaching subquery, as well as added a CTE to filter down Transcipt (biggest table) earlier on.

with dept8 as (
select crsCode, studId from (select studID, crscode from Transcript) A
left join (select crscode from Course where deptId = @v8) B using (crscode)
)

select name, count(*) as n_courses from Student
join dept8 on Student.id = dept8.studId group by name
having count(*) = (select count(*) from Course where deptId = @v8);