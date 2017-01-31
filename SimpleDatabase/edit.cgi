#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
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

SAVE_DIR = "./pictures/"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
	<head>
		<title>Edit</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
	</head>
	<body>
		<div class="header">
			<h1>Edit Picture Title</h1>
		</div>
		<div class="main" id="main">
			%s
			<form>
				<input type="hidden" name="prefix" value="%s">
				Title: <input type="text" name="title" value="%s"><br>
				<input type="submit" name="action" value="Update">
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

def edit_title(form):
	prefix = form.getvalue('prefix')
	txtname = prefix + ".txt"
	f = os.path.join(SAVE_DIR, txtname)
	fin = file(f, 'r')
	title = fin.readline()
	fin.close()
	if not form.has_key('title'):
		print
		print HTML_TEMPLATE % ("<h4>Title cannot be empty</h4>", prefix, title)
		return
	newtitle = form.getvalue('title')
	if not len(newtitle) > 0:
		print
		print HTML_TEMPLATE % ("<h4>Title cannot be empty.</h4>", prefix, title)
		return
	fout = file(f, 'w')
	fout.write(newtitle + "\n")
	fout.close()
	print "Location: gallery.cgi"
	print
	print EMPTY

comment="""
print "content-type: text/html"
form = cgi.FieldStorage();
prefix = form.getvalue('prefix')
if form.has_key('action'):
	value = form.getvalue('action')
	if value == "Update":
		edit_title(form)
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
	print HTML_TEMPLATE % ("", prefix, title)
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
				if value == "Update":
					edit_title(form)
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
				print HTML_TEMPLATE % ("", prefix, title)
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
