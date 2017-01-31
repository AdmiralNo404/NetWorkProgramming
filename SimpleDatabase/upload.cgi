#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import time
import Image
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
<!DOCTYPE html>
<html>
	<head>
		<title>Upload New Photo</title>
		<link rel="stylesheet" type="text/css" href="styles.css" />
		<script type="text/javascript">
			function extValid(input) {
				if (input.type == "file") {
					var filename = input.value;
					if (filename.length > 0) {
						isValid = false;
						ext = filename.substr(filename.length - 5, 5).toLowerCase();
						if (ext == ".jpeg") {
							isValid = true;
						}
						ext = filename.substr(filename.length - 4, 4).toLowerCase();
						if (ext == ".jpg") {
							isValid = true;
						}
						if (!isValid) {
							alert("Invalid file type, please choose a jpg or jpeg file.");
							input.value = "";
							return false;
						}
					}
				}
				return true;
			}
		</script>
	</head>
	<body>
		<div class="header">
			<h1>Upload a New JPEG Picture</h1>
		</div>
		<div class="main" id="main">
			%(MESSAGE)s
			<form method="POST" enctype="multipart/form-data">
				Title: <input type="text" name="title"><br>
				File: <input type="file" name="file_up" onChange="extValid(this);"><br>
				<input type="submit" name="action" value="Upload">
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

UPLOAD_DIR = "./pictures/"

def save_file(form):
	# transfer the file
	field = 'file_up'
	if not form.has_key(field):
		print HTML_TEMPLATE % {'MESSAGE': "<h3>Error: file item not in form</h3>"}
		return
	fileitem = form[field]
	if not fileitem.file or len(fileitem.filename) == 0:
		print HTML_TEMPLATE % {'MESSAGE': "<h3>Error: file not found</h3>"}
		return
	cur_time = str(time.time());
	picname = cur_time + ".jpg"
	f = os.path.join(UPLOAD_DIR, picname)
	fout = file(f, 'w')
	finished = 0
	while not finished:
		chunk = fileitem.file.read(100000)
		if not chunk:
			finished = 1
		else:
			fout.write(chunk)
	fout.close()
	
	# save title
	field = "title"
	if not form.has_key(field):
		print HTML_TEMPLATE % {'MESSAGE': "<h3>Error: text item not in form</h3>"}
		return
	title = form.getvalue('title')
	if len(title) == 0:
		print HTML_TEMPLATE % {'MESSAGE': "<h3>Picture Title Cannot Be Empty</h3>"}
		return
	txtname = cur_time + ".txt"
	f = os.path.join(UPLOAD_DIR, txtname)
	fout = file(f, 'w')
	fout.write(title + "\n")
	fout.close()
	
	# create thumbnail
	size = (140, 140)
	pic_dir = UPLOAD_DIR + picname
	im = Image.open(pic_dir)
	im.thumbnail(size)
	thumb_dir = UPLOAD_DIR + cur_time + "_tn.jpg"
	im.save(thumb_dir, "JPEG")
	
	print HTML_TEMPLATE % {'MESSAGE': "<h3>File upload successful!</h3>"}

comment = """
print "content-type: text/html"
form = cgi.FieldStorage();
if form.has_key('action'):
	value = form.getvalue('action')
	if value == "Upload":
		print
		save_file(form)
	else:
		print "Location: gallery.cgi"
		print
		print EMPTY
else:
	print
	print HTML_TEMPLATE % {'MESSAGE': ""}
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
			if form.has_key('action'):
				value = form.getvalue('action')
				if value == "Upload":
					print
					save_file(form)
				else:
					print "Location: gallery.cgi"
					print
					print EMPTY
			else:
				print
				print HTML_TEMPLATE % {'MESSAGE': ""}
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
