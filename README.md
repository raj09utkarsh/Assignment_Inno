# Summer Intern Hiring Challenge

##
# What does this Application do?
This Program takes input as Email ID of the User and names of TV series.<br/>
The main aim of this program is to send user an email consisting of information regarding when the next episode of these TV series will be aired or when the last episode was aired and description.<br/>

##

# How to use this Program?

### 1. Please verify these points before executing the code.
  * Make sure your system is installed with Mysql and mysqldb python.
  * SMTPLIB should be installed in your system.
  * Your Gmail should allow third party apps(Less secure apps) to send mails.<br/>
  Check this here - [Click here to check](https://www.google.com/settings/security/lesssecureapps). If it is off, then unblock it.
  * You must be connected to the Internate.
  
### 2. Download the main.py file <br/>

### 3. Changes need to be made before running this program
  * <b>In Line no. 11</b> - Enter the hostname, user and password of mysql database. <br/>
  * <b>In Line no. 54 and 55</b> - Enter Sender's Email address and Password in specified format. <br/>
  
### 4. Run python3 main.py in the terminal(After going to specific directory)
  * You have to give the required input in the terminal, such as your email address and TV series you watch.
  * Then you will receive a mail containing all the information about that TV series(Shown below).
  
### Information about some of the TV series has been hardcoded in the python program(For the testing Purpose).
From line 31 to 50.

### What more can be done in the Future : 
  * If suppose the database does not have any details about some specific TV series, Thenusing IMDb API we can update the database and send mail to the Client.
  * Even client can also contribute to the database if the data is not available in the DATABASE, i.e if data is not present then the program will ask the client to enter the missing data and reward points will be given to them.
