# Summer Intern Hiring Challenge
# By Rohit Samudralwar

import MySQLdb
import smtplib


# Open database connection
# Enter the mysql hostname, user and password
# Example db = MySQLdb.connect(host="localhost",user="root",passwd="12345")
db = MySQLdb.connect(host="localhost",user="[root]",passwd="[password]")

# prepare a cursor object using cursor() method
cursor = db.cursor()

query_db= "show databases;"
cursor.execute(query_db)

# Find whether database exits or not
# if not then create one with name : SERIES_DATABASE_1
if ('SERIES_DATABASE_1',) not in cursor:
	# insert_data_into_table(cursor)
	query_cdb = "create database SERIES_DATABASE_1;"
	cursor.execute(query_cdb)
	# selecting database(mysql)
	cursor.execute('use SERIES_DATABASE_1')
	
	query_table = "create table seriesdb(name VARCHAR(30), year INT(4), description VARCHAR(100));"
	cursor.execute(query_table)

	# Hardcoded database only for testing purpose
	query="insert into seriesdb values ('got','2011','Next season will be released in 2019');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('friends','1994','So sorry, The last episode was aired in 2004');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('flash','2014','Next season will be released on 9-Oct 2018');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('sacred games','2018','Next season will be released in Jan 2019');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('game of thrones','2011','Next season will be released in 2019');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('suits','2011','Last video was aired on July-2018');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('black mirror','2011','Next season will be released in 2019');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('breaking bad','2008','So sorry, The last episode was aired in 2013');"
	cursor.execute(query);db.commit()
	query="insert into seriesdb values ('gotham','2014','The next season will start this year');"
	cursor.execute(query);db.commit()

cursor.execute('use SERIES_DATABASE_1')

# Enter the Senders email address and Password below
gmailAddress = 'example@gmail.com'
gmailPassword = 'password'

#Reciver's email address[taken from terminal]
mailTo = input('Enter email address: ')

# Series name separated by comma[taken from terminal]
Input_stream = input('Enter the tv series in comma separated form: ')

# remove all spaces
s = Input_stream.replace(", ", ",")
# Split the string with respect to comma and store in array
TvSeries = s.split(',')

# Message to be sent
msg="\nHello buddy,\nBelow are the details of queries which were asked by you: \n \n"				#Message

# handling queries 
for i in TvSeries:
	try:
		i=i.lower()
		query_to_fetch="select *from seriesdb where name='"+i+"'"
		cursor.execute(query_to_fetch)
		results=cursor.fetchone()
		#add obtained result to message
		msg+='TV series Name='+results[0]+'\n'+'This series was started in - '+str(results[1])+'\n' + 'Status - ' + results[2]+'\n \n'
	except:
		msg+="We dont have any data for TV series '"+i+"'\n"+"If you want to contribute to this DB you can reply to this Thread" +"\n \n"

msg+="\n \n Thanks \n \n"



# Below is code to send mail to the Client using SMTPLIB 

try:
	Sub='Response for your queries '
	Message='Subject:{}\n\n{}'.format(Sub,msg)
	mailServer = smtplib.SMTP('smtp.gmail.com', 587)
	mailServer.starttls()
	mailServer.login(gmailAddress, gmailPassword)
	mailServer.sendmail(gmailAddress, mailTo, Message)
	print(" \n Mail has been sent to your email!\n")
	mailServer.quit()
except:
	print('The mail could not be Sent')

# disconnect from server
db.close()	
