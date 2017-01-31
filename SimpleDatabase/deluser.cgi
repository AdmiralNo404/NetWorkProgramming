#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import Cookie
import time
import MySQLdb

DIR_PATH = "/home/liux1366/.www/4131/assignment5/"
config = "config"
# default values
userID = ""
dbpw = ""
timeout = 0

def readConf():
	f = os.path.join(DIR_PATH, config)
	fin = file(f, 'r')
	# read three lines
	usr = fin.readline()
	pw = fin.readline()
	tostr = fin.readline()
	fin.close()
	# split the line
	usr = usr.split(':')
	usr = usr[1].strip()
	pw = pw.split(':')
	pw = pw[1].strip()
	tostr = tostr.split(':')
	to = int(tostr[1].strip())
	return [usr, pw, to]

plst = readConf()
userID = plst[0]
dbpw = plst[1]
timeout = plst[2]

REDIRECT = """
<!DOCTYPE html>
<html>
	<head>
		<title>Redirect</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
		<meta http-equiv="refresh" content="5;url=menu.cgi" />
	</head>
	<div class="header">
		<body>
			<h3>%(MESSAGE)s</h3>
			<h3>Redirecting in 5 seconds...</h3>
		</body>
	</div>
</html>"""

EMPTY = """
<!DOCTYPE html>
<html>
	<head></head>
	<body></body>
</html>"""

if 'HTTP_COOKIE' in os.environ:
	cookies = os.environ['HTTP_COOKIE']
	cookies = cookies.split(';')
	handler = {}
	for cookie in cookies:
		cookie = cookie.split('=')
		handler[cookie[0].strip()] = cookie[1]
	account = handler['account']
	pw = handler['pw']
	query = 'select Name, Role, Password from Users where Name like "' + account + '"'
	# connect to MySQL
	db = MySQLdb.connect(host="egon.cs.umn.edu", user=userID, passwd=dbpw, port=3307)
	db.select_db(userID)
	cursor = db.cursor()
	cursor.execute(query)
	row = cursor.fetchone()
	if row == None or pw != row[2]:
		print "content-type: text/html"
		print "Location: login.html"
		print
		print EMPTY
	else:
		role = row[1]
		if role == "Owner":
			print "content-type: text/html"
			form = cgi.FieldStorage();
			account = form.getvalue('account')
			query = 'select Name, Role from Users where Name like "' + account + '"'
			cursor.execute(query)
			row = cursor.fetchone()
			if row != None:
				role = row[1]
				if role == "Owner":
					print
					print REDIRECT % {'MESSAGE': "Cannot delete owner account!"}
				else:
					delete = 'delete from Users where Name like "' + account + '"'
					cursor.execute(delete)
					db.commit()
					print
					print REDIRECT % {'MESSAGE': "User account sucessfully deleted!"}
			else:
				print
				print REDIRECT % {'MESSAGE': "User name does not exist!"}
		elif role == "Visitor":
			print "content-type: text/html"
			print "Location: gallery.cgi"
			print
			print EMPTY
else:
	print "content-type: text/html"
	print "Location: login.html"
	print
	print EMPTY
