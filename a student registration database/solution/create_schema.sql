--Pengxiang Jia--
--V00835664    --

drop table if exists prerequisites cascade;
drop table if exists enrollments cascade;
drop table if exists course_offerings cascade;
drop table if exists courses cascade;
drop table if exists students cascade;
drop function if exists student_insertion_duplicated_trigger();
drop function if exists course_max_capacity_trigger();
drop function if exists enrollment_condition_trigger();
drop function if exists drop_course_grade_trigger();
drop function if exists course_insertion_duplicated_trigger();
drop function if exists prerequisite_insertion_duplicated_trigger();
drop function if exists assigning_grade_trigger();

create table students(
	student_id varchar(9) check(student_id similar to 'V00[0-9]+' and length(student_id) = 9) primary key,
	student_name varchar(255) check(length(student_name) > 0)
	);
	
create table courses(
	course_code varchar(10) primary key
	);
	
create table course_offerings(
	course_code varchar(10),
	course_name varchar(128) not null,
	term_code varchar(6) check(length(term_code) = 6),
	instructor_name varchar(255) check(length(instructor_name) > 0),
	max_capacity integer check(max_capacity >= 0),
	primary key (course_code, term_code),
	foreign key (course_code) references courses(course_code)
		on delete restrict
		on update cascade
	);

create table prerequisites(
	course_code varchar(10),
	prereq_course_code varchar(10),
	term_code varchar(6),
	primary key(course_code, prereq_course_code, term_code),
	foreign key (course_code, term_code) references course_offerings(course_code, term_code)
		on delete restrict
		on update cascade,
	foreign key (prereq_course_code) references courses(course_code)
		on delete restrict
		on update cascade
	);

create table enrollments(
	student_id varchar(9),
	course_code varchar(10),
	term_code varchar(6),
	grade integer check(grade > 0 and  grade < 100),
	primary key (student_id, course_code, term_code),
	foreign key (student_id) references students(student_id)
		on delete restrict
		on update cascade,
	foreign key (course_code,term_code) references course_offerings(course_code, term_code)
		on delete restrict
		on update cascade
	);

---------------------------------------------------------------------------------------------------------------------
create function student_insertion_duplicated_trigger()
returns trigger as
$BODY$
begin
if (select count(*) 
		from students 
		where student_id = new.student_id) = 1
then
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger student_insertion_duplicated_constraint
	before insert or update on students
	for each row
	execute procedure student_insertion_duplicated_trigger();
----------------------------------------------------------------------------------------------------------------------------------------------------

create function course_insertion_duplicated_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from courses where course_code = new.course_code) = 1
then
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger course_insertion_duplicated_constraint
	before insert or update on courses
	for each row
	execute procedure course_insertion_duplicated_trigger();

------------------------------------------------------------------------------------------------------------------------------------------------------------

create function prerequisite_insertion_duplicated_trigger()
returns trigger as
$BODY$
begin
if (select count(*) from prerequisites 
		where course_code = new.course_code 
		and term_code = new.term_code 
		and prereq_course_code = new.prereq_course_code) = 1
then
	return null;
end if;
return new;
end
$BODY$
language plpgsql;

create trigger course_insertion_duplicated_constraint
	before insert or update on prerequisites
	for each row
	execute procedure prerequisite_insertion_duplicated_trigger();

---------------------------------------------------------------------------------------------------------------------

create function drop_course_grade_trigger()
returns trigger as 
$BODY$
begin
if (select count(*) from enrollments 
	where student_id = old.student_id 
	and course_code = old.course_code 
	and term_code = old.term_code 
	and grade is not null) = 1
then
	raise exception 'Can not drop the course with grade.';
end if;
return new;	
end 
$BODY$
language plpgsql;

create trigger drop_course_constraint
	before delete on enrollments
	for each row 
	execute procedure drop_course_grade_trigger();

----------------------------------------------------------------------------------------------------------------------------------------------------
create function enrollment_condition_trigger()
returns trigger as 
$BODY$
begin
if (select count(*) from enrollments where 
	student_id = new.student_id and 
	course_code = new.course_code and 
	term_code = new.term_code
	and grade = new.grade) = 1
then
	return null;
end if;

if (select count(*) from enrollments 
			where course_code = new.course_code 
			and term_code = new.term_code) 
	= (select max_capacity from course_offerings 
			where course_code = new.course_code 
			and term_code = new.term_code)
then
	raise exception 'There is one course that the student try to register is already full.';
end if;

if (select count(distinct course_code) from 
			(select course_code 
				from enrollments 
				where student_id = new.student_id) as student_enrolled_courses 
			natural join 
			(select prereq_course_code as course_code 
				from prerequisites 
				where course_code = new.course_code 
				and term_code = new.term_code) as prereq_courses) 
		< 
			(select count(*) 
			   from prerequisites 
				where course_code = new.course_code 
				and term_code = new.term_code)
	then
		raise exception 'There is at least one prerequisite course that student has never taken.';
	else
		if (select count(distinct enrollments.course_code) from 
				enrollments
				where enrollments.student_id = new.student_id 
				and enrollments.term_code < new.term_code 
				and (grade is null or grade > 50)) 
			< 
				(select count(*) from prerequisites 
					where course_code = new.course_code and term_code = new.term_code)
		then	
			raise exception 'One prerequisite the student has taken but failed and is not attempting before registering the course requiring it';
		end if;
end if;

return new;
end 
$BODY$
language plpgsql;

create trigger enrollment_condition_constraint
	before insert or update on enrollments
	for each row 
	execute procedure enrollment_condition_trigger();

