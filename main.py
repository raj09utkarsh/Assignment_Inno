# Summer Intern Hiring Challenge
# By Rohit Samudralwar
# Please refer Read_Me file sent with this Assignment

import sys
import MySQLdb
import smtplib
from requests import get
import urllib.request
from bs4 import BeautifulSoup
import requests
import unicodedata
import datetime

# code to return HTML Soup for the given url(using 'BeautifulSoup')
def give_html_file(curr_url):
	response = get(curr_url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	# convert the soup into text
	text=response.text
	return text


# Code to find whether the series is finished or not
def series_finished_or_not(url_imdb):
	imdb_text = give_html_file(url_imdb)
	# to find the phrase 'See more release dates'
	find_date_ind = imdb_text.find("See more release dates")
	
	# finds start year of the season
	start_date_ind = find_date_ind
	while imdb_text[start_date_ind]!='(':
		start_date_ind+=1
	start_date_ind+=1

	#finds end year of the series(if the series is finished)
	end_date_ind = start_date_ind+5

	start_date = imdb_text[start_date_ind:start_date_ind + 4]
	end_date = imdb_text[end_date_ind:end_date_ind + 4]

	# Is series is finished of not?
	if end_date[0]==' ':
		return 'notfinished'
	else:
		return 'finished'

# Dictionary to get the corresponding number for month.  	
def find_month(mon):
	mon_map = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
	return str(mon_map[mon])

# Code to find the next episode date.
def find_next_episode_date(episode_url):
	# Get HTML Soup
	response = get(episode_url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	
	# find all classes with name 'airdate'
	air_date = html_soup.find_all('div', class_ = 'airdate')
	
	# strr contains all the dates in the corresponding html page.
	strr=""
	for i in air_date:
		strr+=i.get_text()
	strr=strr.replace(" ","")
	strr=strr.replace("\n\n","\n")
	dates = strr.split("\n")
	
	# removing blanck dates
	while '' in dates:
		dates.remove('')
	
	ind=0
	for i in dates:
		st=i.replace('.','') 

		# if the string length is less than 4, no use.
		if len(st)<4:
			continue

		# if the string length is between 4:7, then date is in year format(no need to edit)
		if len(st)<7:
			ind+=1
			continue

		# if the string length is between 4:7, then convert it into format : 'YYYYMMDD' 
		space=""
		if len(st) == 8:
			space="0"
		st = st[len(st)-4:len(st)] + st[len(st)-7:len(st)-4] +space+ st[0:len(st)-7]
		st=st.replace(st[4:7],find_month(st[4:7]))
		
		dates[ind]=st;ind+=1;

	dates=dates[0:ind]

	# current date
	now = datetime.datetime.now()
	curr_date  = str(now.year) + str(now.month) + str(now.day)
	
	# finding the date next to current date.
	ind=0
	while dates[ind]<curr_date and ind+1<len(dates) and len(dates[ind])>4:
		ind+=1 
	next_episode_date = dates[ind]
	return next_episode_date		


def find_current_season_url(page_url):
	response = get(page_url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	season = html_soup.find('div', class_ = 'seasons-and-year-nav')
	tags_href = season.find_all(lambda tag: tag.name == 'a' and tag.get('href') and tag.text)
	first_link = tags_href[0].attrs['href']
	return 'https://www.imdb.com' + first_link

def find_series_url(name):
	name.replace(" ","+")
	page_url = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + name + "&s=all"
	response = get(page_url)
	html_soup = BeautifulSoup(response.text, 'html.parser')
	first_result = html_soup.find('table', class_ = 'findList')
	tags_href = first_result.find_all(lambda tag: tag.name == 'a' and tag.get('href') and tag.text)
	first_link = tags_href[0].attrs['href']
	return 'https://www.imdb.com' + first_link

def store_in_db(mailTo,series_names):
	try:
		# Open database connection
		# Enter the mysql hostname, user and password
		# Example db = MySQLdb.connect(host="localhost",user="root",passwd="12345")
		db = MySQLdb.connect(host="localhost",user="root",passwd="1111")

		# prepare a cursor object using cursor() method
		cursor = db.cursor()

		query_db= "show databases;"
		cursor.execute(query_db)

		# Find whether database exits or not
		# if not then create one with name : 'SERIES_DATABASE_1'
		if ('SERIES_DATABASE_1u',) not in cursor:
			# insert_data_into_table(cursor)
			query_cdb = "create database SERIES_DATABASE_1u;"
			cursor.execute(query_cdb)
			# selecting database(mysql)
			cursor.execute('use SERIES_DATABASE_1u')
			
			# create table with name : 'userdata'
			query_table = "create table userdata(email VARCHAR(30),tvseries VARCHAR(500));"
			cursor.execute(query_table)

		cursor.execute('use SERIES_DATABASE_1u')
	except:
		print('Error\n')

	#Query to insert details into DATABASE.
	query="insert into userdata values ('" + mailTo + "','"+ series_names + "');"
	cursor.execute(query);db.commit()
	db.close()

def send_mail(mailTo,msg):
	print('\nSending mail...!\n') 

	# Enter the Senders email address and Password below
	gmailAddress = 'example.new.someone@gmail.com'		# The default Id-password are working
	gmailPassword = 'qwerty@123'
	
	# Below is code to send mail to the Client using SMTPLIB 
	try:
		Sub='Response for your queries '
		Message='Subject:{}\n\n{}'.format(Sub,msg)
		mailServer = smtplib.SMTP('smtp.gmail.com', 587)
		mailServer.starttls()
		mailServer.login(gmailAddress, gmailPassword)
		mailServer.sendmail(gmailAddress, mailTo, Message)
		print(" \nMail has been sent to your email!\n")
		mailServer.quit()
	except:
		print('Sorry, The mail could not be Sent \n \n')

# ----------------------------------------------------------------------------------------------------------
# Main Function

#Reciver's email address[taken from terminal]
mailTo = input('Enter email address: ')
# Series name separated by comma[taken from terminal]
series_names = input('Enter the tv series in comma separated form: ')

# function to store the details in the DATABASE
try:
	store_in_db(mailTo,series_names)
except:
	print('There is error in establishing the DATABASE connection.\nMake sure your system is installed with mysql and python\n \nTrying to send mail. \n \n')
		
# Collecting all TV series in array
series_names = series_names.replace(', ',',')
tvseries = series_names.split(",")

print('\nFinding the information...\n')
# Message
msg="\nHello buddy,\nBelow are the details of queries which were asked by you: \n \n"				

for name in tvseries:
	# current date
	now = datetime.datetime.now()
	curr_date = str(now.year) + str(now.month) + str(now.day)
	msg+='TV series name - '+ name+"\n"
	try:
		# Searching the TV series in imdb and returning the first result.
		series_url = find_series_url(name)
		# Finding the current season going on
		curr_season_url = find_current_season_url(series_url)
		# Function that returns the next episode of the TV Series.
		try:
			next_episode_date = find_next_episode_date(curr_season_url)
		except:
			msg+="Next season will begin in year "+ str(now.year + 1)+"\n"
			continue 
		# Finding wherher the TV series finished its all episodes or not. 
		finish = series_finished_or_not(series_url)		

		next_episode_date_in_format = next_episode_date[6:8] + "-" + next_episode_date[4:6] + "-" + next_episode_date[0:4]
	except:
		msg+='Entered the wrong name, Please check the spelling.\n \n'
		continue
	# If the TV series is finished.
	if finish=='finished':
		msg+='The show has finished streaming all its episodes.\n \n'
	elif len(next_episode_date) == 4:
		# if the season is going on but, exact dates are not mentioned.
		# else the next season will begin in the given year.
		if next_episode_date[0:4] == str(now.year):
			msg+='Next epiosde will be aired in ' + str(now.year) + ' but we dont have the exact dates.\n \n'
		else:
			msg+='Next season will begin in year ' + next_episode_date[0:4]+"\n \n"
	# If the next episode date mentioned in Website is gone.
	elif next_episode_date < curr_date:
		msg+='We dont have any data for the next episode, but the Series is currently running. \nThe last episode was aired on '+next_episode_date_in_format + " \n \n"
	# Next episode date for the TV Series.
	elif len(next_episode_date) == 8:
		msg+='The next episode airs on ' + next_episode_date_in_format + "\n \n"

msg+="\n \nThanks and Regards,\nRohit Samudralwar \n \n"
# print(msg)
print('All set...!')
# Function to send mail.
send_mail(mailTo,msg)
