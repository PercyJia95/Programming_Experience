# report_classlist.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_classlist.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018

import psycopg2, sys

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)) )
	print("  Term %s"%(str(term), ) )
	print("  Instructor: %s"%(str(instructor_name), ) )
	
def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)) )
	else:
		print("%10s %-25s"%(str(student_id), str(student_name),) )

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity)) )


''' The lines below would be helpful in your solution
if len(sys.argv) < 3:
	print('Usage: %s <course code> <term>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
course_code, term = sys.argv[1:3]
'''


# Mockup: Print a class list for CSC 370
# course_code = 'CSC 370'
# course_name = 'Database Systems'
# course_term = 201801
# instructor_name = 'Bill Bird'
# print_header(course_code, course_name, course_term, instructor_name)

# Print records for a few students
# print_row('V00123456', 'Rebecca Raspberry', 81)
# print_row('V00123457', 'Alissa Aubergine', 90)
# print_row('V00123458', 'Neal Naranja', 83)

# Print the last line (enrollment/max_capacity)
# print_footer(3,150)

psql_user = 'jiapx'
psql_db = 'jiapx'
psql_password = 'V00835664'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("""select course_name, instructor_name, students.student_id, student_name, grade, max_capacity 
					from enrollments 
						natural join 
					students 
						natural join 
					course_offerings  
					where enrollments.course_code = %s 
					and enrollments.term_code = %s 
					order by students.student_id asc;""", (sys.argv[1], sys.argv[2]))

row = cursor.fetchone()

if row is None:
	print("Error: Student %s not found.")
else:
	print_header(sys.argv[1], row[0], sys.argv[2], row[1])
	capacity = row[5]
	num_enrolled = 1

	while True:
		print_row(row[2], row[3], row[4])
		row = cursor.fetchone()
		if row is None:
			break
		num_enrolled += 1
	
	print_footer(num_enrolled , capacity)


cursor.close()
conn.close()