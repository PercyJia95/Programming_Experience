# add_drop.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
#
# B. Bird - 02/26/2018

import sys, csv, psycopg2


psql_user = 'jiapx' #Change this to your username
psql_db = 'jiapx'
psql_password = 'V00835664' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

if len(sys.argv) < 2:
	print("Usage: %s <input file>",file=sys.stderr)
	sys.exit(0)
	
input_filename = sys.argv[1]

# Open your DB connection here
conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

with open(input_filename) as f:
	for row in csv.reader(f):
		if len(row) == 0:
			continue #Ignore blank rows
		if len(row) != 5:
			print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			conn.rollback();
			break
		add_or_drop,student_id,student_name,course_code,term = row
		#Do something with the data here
		#Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
		try:	
			if add_or_drop == 'ADD':
				insert_statement = cursor.mogrify("insert into students values(%s, %s);", (student_id, student_name))
				cursor.execute(insert_statement)
				insert_statement = cursor.mogrify("insert into enrollments values(%s, %s, %s);", (student_id, course_code, term))
				cursor.execute(insert_statement)
			if add_or_drop == 'DROP':
				drop_statement = cursor.mogrify("delete from enrollments where student_id = %s and course_code = %s and term_code = %s;", (student_id,course_code,term))
				cursor.execute(drop_statement)

			conn.commit() #Only commit if no error occurs (commit will actually be prevented if an error occurs anyway)
		except psycopg2.ProgrammingError as err: 
			#ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
			print("Caught a ProgrammingError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.IntegrityError as err: 
			#IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.InternalError as err:  			
			#InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
			#In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
			#(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
cursor.close()
conn.close()		
		