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

-- 5. List the names of students who have taken a course from department v6 (deptId), but not v7.
SELECT * FROM Student, 
	(SELECT studId FROM Transcript, Course WHERE deptId = @v6 AND Course.crsCode = Transcript.crsCode
	AND studId NOT IN
	(SELECT studId FROM Transcript, Course WHERE deptId = @v7 AND Course.crsCode = Transcript.crsCode)) as alias
WHERE Student.id = alias.studId;

--Optimized query
with subset as (
select studId, deptId from Transcript join (select crsCode, deptId from Course 
	where deptId in (@v6,@v7)) B using (crsCode)
)

select name from Student 
where id in (select studId from subset where deptId=@v6) 
and id not in (select studId from subset where deptId=@v7);

--Using a CTE means we only have to join transcipt to course once instead of twice, then we use
-- the smaller dataset for filtering on deptID later. Furthermore, using IN is more efficient that the
--correlated subqueries. The original query also returns duplicate and incorrect results.