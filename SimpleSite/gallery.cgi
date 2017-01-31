#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()

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
				<input type="submit" name="action" value="Refresh">
				<input type="submit" name="action" value="Upload New Picture">
			</form>
		</div>
		<div class="canvas">
			%(BLOCK)s
		</div>
	</body>
</html>""" #changed one line in this block

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

EMPTY = """
<!DOCTYPE html>
<html>
	<head></head>
	<body></body>
</html>"""

SERVER_URL = "./pictures/" #changed here
SAVE_DIR = "./pictures/" #changed here

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
	print HTML_TEMPLATE  % {'BLOCK': DIV_CONTENT}

print "content-type: text/html"
form = cgi.FieldStorage();
if form.has_key('action'):
	value = form.getvalue('action')
	if value == "Upload New Picture":
		print "Location: upload.cgi"
		print
		print EMPTY
	else:
		print "Location: gallery.cgi"
		print
		print EMPTY
else:
	print
	thumbs_gen()
