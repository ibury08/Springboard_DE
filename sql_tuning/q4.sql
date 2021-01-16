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

-- 4. List the names of students who have taken a course taught by professor v5 (name).
SELECT name FROM Student,
	(SELECT studId FROM Transcript,
		(SELECT crsCode, semester FROM Professor
			JOIN Teaching
			WHERE Professor.name = @v5 AND Professor.id = Teaching.profId) as alias1
	WHERE Transcript.crsCode = alias1.crsCode AND Transcript.semester = alias1.semester) as alias2
WHERE Student.id = alias2.studId;


--Optimized Query
select C.name from Transcript 
join (select crsCode, semester from Teaching where profId in 
	(select id from Professor where name = @v5)) B 
join (select id, name from Student) C 
on Transcript.crsCode = B.crsCode 
and Transcript.semester = B.semester 
and C.id=Transcript.studId;

-- Note: this query returns an empty set. There are rows for students in the same course number as the
-- one taught by this professor, albeit in a different semester.
-- Replacing the nested correlated subqueries with joins makes this more efficient.