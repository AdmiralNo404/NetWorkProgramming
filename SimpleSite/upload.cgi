#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import time
import Image

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

UPLOAD_DIR = "./pictures/" #changed here

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
