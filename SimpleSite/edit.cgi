#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()

SAVE_DIR = "./pictures/" #changed here

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
