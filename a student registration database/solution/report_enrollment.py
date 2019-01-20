# report_enrollment.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_enrollment.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018

import psycopg2, sys

psql_user = 'jiapx'
psql_db = 'jiapx'
psql_password = 'V00835664'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

def print_row(term, course_code, course_name, instructor_name, total_enrollment, maximum_capacity):
	print("%6s %10s %-35s %-25s %s/%s"%(str(term), str(course_code), str(course_name), str(instructor_name), str(total_enrollment), str(maximum_capacity)) )

cursor.execute(""" select course_offerings.term_code, course_offerings.course_code, course_name, instructor_name, count(*) as total_enrollment, max_capacity 
					  from course_offerings 
							left outer join
						  enrollments
						  on course_offerings.course_code = enrollments.course_code
						  and course_offerings.term_code = enrollments.term_code
					  group by course_offerings.course_code, course_offerings.term_code, instructor_name
					  order by term_code, course_code;
			   """)

while True:
	row = cursor.fetchone()
	if row is None:
		break
	print_row(row[0], row[1], row[2], row[3], row[4], row[5])

cursor.close()
conn.close()