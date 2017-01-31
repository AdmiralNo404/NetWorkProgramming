#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()

SAVE_DIR = "./pictures/" #changed here

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
