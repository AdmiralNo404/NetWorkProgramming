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

HTML_TEMPLATE = """
<!DOCTYPE HTML>
<html>
	<head>
		<title>Gallery</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
		<script type="text/javascript">
			function openImg(filename, title) {
				var div_pop = document.getElementById("popup");
				var w = window.innerWidth;
				var h = window.innerHeight;
				var setAttr = "width: " + w + "px; height: " + h + "px";
				div_pop.setAttribute("style", setAttr);
				div_pop.innerHTML = '<h1>' + title + '</h1><img src="./pictures/'
									+ filename + '" alt="Large Image" class="large">';
			}
			function closeImg() {
				var div_pop = document.getElementById("popup");
				div_pop.setAttribute("style", "width: 0px; height: 0px");
				div_pop.innerHTML = "";
			}
		</script>
	</head>
	<body>
		<div id="popup" class="popup" onClick="closeImg()"></div>
		<div class="header">
			<h1>Picture Gallery</h1>
			<form class="button">
				<input type="submit" value="Refresh" formaction="gallery.cgi">
				<input type="submit" value="Upload New Picture" formaction="upload.cgi">
			</form>
		</div>
		<div class="canvas">
			%(BLOCK)s
		</div>
	</body>
</html>"""

HTML_TEMPLATE_V = """
<!DOCTYPE HTML>
<html>
	<head>
		<title>Gallery</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
		<script type="text/javascript">
			function openImg(filename, title) {
				var div_pop = document.getElementById("popup");
				var w = window.innerWidth;
				var h = window.innerHeight;
				var setAttr = "width: " + w + "px; height: " + h + "px";
				div_pop.setAttribute("style", setAttr);
				div_pop.innerHTML = '<h1>' + title + '</h1><img src="./pictures/'
									+ filename + '" alt="Large Image" class="large">';
			}
			function closeImg() {
				var div_pop = document.getElementById("popup");
				div_pop.setAttribute("style", "width: 0px; height: 0px");
				div_pop.innerHTML = "";
			}
		</script>
	</head>
	<body>
		<div id="popup" class="popup" onClick="closeImg()"></div>
		<div class="header">
			<h1>Picture Gallery</h1>
			<form class="button">
				<input type="submit" value="Refresh" formaction="gallery.cgi">
			</form>
		</div>
		<div class="canvas">
			%(BLOCK)s
		</div>
	</body>
</html>"""

THUMB_TEMPLATE = """
<div class="thumbs">
	<img class="thumb" src="%s" alt="%s" onClick="openImg('%s', '%s')">
	<h4>%s</h4>
	<form class="button">
		<input type="hidden" name="prefix", value="%s">
		<input type="submit" value="Delete" formaction="delete.cgi">
		<input type="submit" value="Edit" formaction="edit.cgi">
	</form>
</div>"""

THUMB_TEMPLATE_V = """
<div class="thumbs">
	<img class="thumb" src="%s" alt="%s" onClick="openImg('%s', '%s')">
	<h4>%s</h4>
</div>"""

EMPTY = """
<!DOCTYPE html>
<html>
	<head></head>
	<body></body>
</html>"""

SERVER_URL = "./pictures/"
SAVE_DIR = "./pictures/"

def thumbs_gen():
	DIV_CONTENT = ""
	filelist = os.listdir(SAVE_DIR)
	for filename in filelist:
		ext = filename[-7:]
		prefix = filename[:-7]
		file_url = SERVER_URL + filename
		if ext == "_tn.jpg":
			txtname = prefix + ".txt"
			picname = prefix + ".jpg"
			f = os.path.join(SAVE_DIR, txtname)
			fin = file(f, 'r')
			title = fin.readline()
			title = title[:-1];
			CONTENT = THUMB_TEMPLATE % (file_url, title, picname, title, title, prefix)
			DIV_CONTENT = DIV_CONTENT + CONTENT
	print "content-type: text/html"
	print
	print HTML_TEMPLATE  % {'BLOCK': DIV_CONTENT}

def thumbs_gen_v():
	DIV_CONTENT = ""
	filelist = os.listdir(SAVE_DIR)
	for filename in filelist:
		ext = filename[-7:]
		prefix = filename[:-7]
		file_url = SERVER_URL + filename
		if ext == "_tn.jpg":
			txtname = prefix + ".txt"
			picname = prefix + ".jpg"
			f = os.path.join(SAVE_DIR, txtname)
			fin = file(f, 'r')
			title = fin.readline()
			title = title[:-1];
			CONTENT = THUMB_TEMPLATE_V % (file_url, title, picname, title, title)
			DIV_CONTENT = DIV_CONTENT + CONTENT
	print "content-type: text/html"
	print
	print HTML_TEMPLATE_V  % {'BLOCK': DIV_CONTENT}

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
			thumbs_gen()
		elif role == "Visitor":
			thumbs_gen_v()
else:
	print "content-type: text/html"
	print "Location: login.html"
	print
	print EMPTY
