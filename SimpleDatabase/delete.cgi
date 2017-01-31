#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import time
import MySQLdb

DIR_PATH = "./"
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

SAVE_DIR = "./pictures/"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
	<head>
		<title>Delete</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
	</head>
	<body>
		<div class="header">
			<h1>Delete Picture</h1>
		</div>
		<div class="main" id="main">
			<p>Are you sure you want to delete picture [ %s ]?</p>
			<form>
				<input type="hidden" name="prefix" value="%s">
				<input type="submit" name="action" value="Delete">
				<input type="submit" name="action" value="Cancel">
			</form>
		</div>
	</body>
</html>"""

EMPTY = """
<!DOCTYPE html>
<html>
	<head></head>
	<body></body>
</html>"""

def delete_file(prefix):
	# first delete picture
	picname = prefix + ".jpg"
	os.remove(SAVE_DIR + picname)
	
	# then remove thumbnail
	thumbname = prefix + "_tn.jpg"
	os.remove(SAVE_DIR + thumbname)
	
	# last remove txt
	txtname = prefix + ".txt"
	os.remove(SAVE_DIR + txtname)

comment="""
print "content-type: text/html"
form = cgi.FieldStorage();
prefix = form.getvalue('prefix')
if form.has_key('action'):
	value = form.getvalue('action')
	if value == "Delete":
		delete_file(prefix)
		print "Location: gallery.cgi"
		print
		print EMPTY
	else:
		print "Location: gallery.cgi"
		print
		print EMPTY
else:
	txtname = prefix + ".txt"
	f = os.path.join(SAVE_DIR, txtname)
	fin = file(f, 'r')
	title = fin.readline()
	fin.close()
	print
	print HTML_TEMPLATE % (title, prefix)
"""

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
			prefix = form.getvalue('prefix')
			if form.has_key('action'):
				value = form.getvalue('action')
				if value == "Delete":
					delete_file(prefix)
					print "Location: gallery.cgi"
					print
					print EMPTY
				else:
					print "Location: gallery.cgi"
					print
					print EMPTY
			else:
				txtname = prefix + ".txt"
				f = os.path.join(SAVE_DIR, txtname)
				fin = file(f, 'r')
				title = fin.readline()
				fin.close()
				print
				print HTML_TEMPLATE % (title, prefix)
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
