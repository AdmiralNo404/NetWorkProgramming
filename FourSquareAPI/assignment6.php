<!DOCTYPE html>
<html>
	<head>
		<title> FourSquare </title>
		<meta name="viewport" content="initial-scale=1.0">
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="styles.css">
	</head>
	<body>
		<div id="panel">
			<form method ="POST" id="cate" onSubmit="return formHandler()">
				<input type="checkbox" name="AE" id="AE">Atrs & Entertainment<br>
				<input type="checkbox" name="food" id="food">Food<br>
				<input type="checkbox" name="NL" id="NL">Nightlife Spot<br>
				<input type="checkbox" name="OR" id="OR">Outdoors & Recreation<br>
				<input type="checkbox" name="SS" id="SS">Shop & Service<br>
				<input type="checkbox" name="TT" id="TT">Travel & Transport<br>
				<input type="checkbox" name="CU" id="CU">College & University<br>
				<input type="checkbox" name=POP" id="POP">Professional & Other Places<br>
				<input type="checkbox" name="R" id="R">Residence<br>
				Limit (K):<br>
				<input type="range" id="limitr" name="limit" min="0" max="50" value="25" onchange="updateTextInput(this.value, this.name)"><br>
				<input type="text" id="limit" value="25" readonly><br>
				Radius(M):<br>
				<input type="range" id="radiusr" name="radius" min="0" max="3000" step="100" value="1500" onchange="updateTextInput(this.value, this.name)"><br>
				<input type="text" id="radius" value="1500" readonly><br>
				<br>
				<input type="hidden" id="lat" name="lat" value="">
				<input type="hidden" id="lng" name="lng" value="">
				<input type="submit">
			</form>
		</div>
		<div id="map"></div>
		<script>
			var map;
			var venues = [];
			var infoWindows = [];

			var newMarker;
			function addMarker(location, map) {
				if (newMarker != null) {
					newMarker.setMap(null);
				}
				title = "(" + location.lat() + ", " + location.lng() + ")";
				newMarker = new google.maps.Marker( {
					position: location,
					map: map,
					title: title
				});
				
				document.getElementById('lat').value = location.lat();
				document.getElementById('lng').value = location.lng();
			}

			function initialize() {
				var docLat = document.getElementById('lat');
				var docLng = document.getElementById('lng');
				// set checkboxes
				<?php if(isset($_POST['AE'])) { echo "document.getElementById('AE').checked = 'checked';"; } ?>
				<?php if(isset($_POST['food'])) { echo "document.getElementById('food').checked = 'checked';"; } ?>
				<?php if(isset($_POST['NL'])) { echo "document.getElementById('NL').checked = 'checked';"; } ?>
				<?php if(isset($_POST['OR'])) { echo "document.getElementById('OR').checked = 'checked';"; } ?>
				<?php if(isset($_POST['SS'])) { echo "document.getElementById('SS').checked = 'checked';"; } ?>
				<?php if(isset($_POST['TT'])) { echo "document.getElementById('TT').checked = 'checked';"; } ?>
				<?php if(isset($_POST['CU'])) { echo "document.getElementById('CU').checked = 'checked';"; } ?>
				<?php if(isset($_POST['POP'])) { echo "document.getElementById('POP').checked = 'checked';"; } ?>
				<?php if(isset($_POST['R'])) { echo "document.getElementById('R').checked = 'checked';"; } ?>
				
				// set range bars
				document.getElementById('limitr').value = "<?php echo isset($_POST['limit']) ? htmlentities($_POST['limit']) : 25; ?>";
				document.getElementById('limit').value = "<?php echo isset($_POST['limit']) ? htmlentities($_POST['limit']) : 25; ?>";
				document.getElementById('radiusr').value = "<?php echo isset($_POST['radius']) ? htmlentities($_POST['radius']) : 1500; ?>";
				document.getElementById('radius').value = "<?php echo isset($_POST['radius']) ? htmlentities($_POST['radius']) : 1500; ?>";
				
				// get submitted location (if there is)
				docLat.value = "<?php echo isset($_POST['lat']) ? $_POST['lat'] : null; ?>";
				docLng.value = "<?php echo isset($_POST['lng']) ? $_POST['lng'] : null; ?>";	
				
				// create map centered around the query marker (if there is)
				if ((docLat.value == "") || (docLng.value == "")) {
					map = new google.maps.Map(document.getElementById('map'), {
						center: {lat: 44.977, lng: -93.235},
						zoom: 15
					});
				} else {
					map = new google.maps.Map(document.getElementById('map'), {
						center: {lat: parseFloat(docLat.value), lng: parseFloat(docLng.value)},
						zoom: 15
					});
				}
				
				// set query marker
				<?php 
					if(isset($_POST['lat']) && isset($_POST['lng'])) {
						// set title
						$marker_title = "(".$_POST['lat'].", ".$_POST['lng'].")";
						// create marker
						echo "newMarker = new google.maps.Marker( {
								position: new google.maps.LatLng(docLat.value, docLng.value), 
								map: map, 
								title: '".$marker_title."' });";
					}
				?>

				google.maps.event.addListener(map, 'click', function(event) {
					addMarker(event.latLng, map);
				});
				
				/********************** Any essential functions goes above this line ************************/
				/************************************************************************************************/
				// execute the following code only if lat and lng have values now
				// else return
				if ((docLat.value == "") || (docLng.value == "")) {
					return;
				}
				
				<?php
					$token = 'KDRNKQNWCDUVFDIYVS32CTKUP3L2VXXK2OKDDOLAFZUGAKMA';
					$date = "20151119";
					$categories = array('AE', 'food', 'NL', 'OR', 'SS', 'TT', 'CU', 'POP', 'R');
					$CateID = array('4d4b7104d754a06370d81259',
									'4d4b7105d754a06374d81259',
									'4d4b7105d754a06376d81259',
									'4d4b7105d754a06377d81259',
									'4d4b7105d754a06378d81259',
									'4d4b7105d754a06379d81259',
									'4d4b7105d754a06372d81259',
									'4d4b7105d754a06375d81259',
									'4e67e38e036454776db1fb3a' );
					
					// get lat and lng
					$lat = $_POST['lat'];
					$lng = $_POST['lng'];
					// get checked categories
					$num = 0;
					$selected = array();
					for ($i = 0; $i < 9; $i++) {
						$cid = $categories[$i];
						if (isset($_POST[$cid])) {
							array_push($selected, $CateID[$i]);
							$num = $num + 1;
						}
					}
					// get limit and radius
					$limit = $_POST['limit'];
					$radius = $_POST['radius'];
					// parse categori string
					$cateStr = "";
					if ($num == 0) {
						$cateStr = implode(",", $CateID);
					} else {
						$cateStr = implode(",", $selected);
					}
					// post request to foursquare
					$temp = array('https://api.foursquare.com/v2/venues/search?ll=',
								$lat, ',', $lng,
								'&intent=browse&oauth_token=',
								$token,
								'&limit=', $limit, '&radius=', $radius,
								'&categoryId=',
								$cateStr,
								'&v=', $date);
					$request = implode("", $temp);
					
					$json = file_get_contents($request);
					$json_data = json_decode($json);
					$response = $json_data->response;
					$result = $response->venues;
					
					$max = count($result);
					// prepare some arrays
					$names = array();
					$address = array();
					$latArray = array();
					$lngArray = array();
					$iconURL = array();
					for ($i = 0; $i < $max; $i++) {
						$venue = $result[$i];
						// get name
						array_push($names, $venue->name);
						// get location
						$loc = $venue->location;
						// get address
						array_push($address, $loc->address);
						// get lat lng
						array_push($latArray, $loc->lat);
						array_push($lngArray, $loc->lng);
						// get icon URL
						$icon = $venue->categories[0]->icon;
						array_push($iconURL, $icon->prefix.'bg_32'.$icon->suffix);
					}
				?>
				
				var max = "<?php echo $max; ?>";
				if (max == 0) {
					//alert("No result found!");
					return;
				}
								
				var names = [];
				<?php
					foreach ($names as $n) {
						echo 'names.push("'.$n.'");';
					}
				?>
				
				var address = [];
				<?php
					foreach ($address as $a) {
						echo 'address.push("'.$a.'");';
					}
				?>
				
				var latArray = [];
				<?php
					foreach ($latArray as $lat) {
						echo 'latArray.push("'.$lat.'");';
					}
				?>
				
				var lngArray = [];
				<?php
					foreach ($lngArray as $lng) {
						echo 'lngArray.push("'.$lng.'");';
					}
				?>
				
				var iconURL = [];
				<?php
					foreach ($iconURL as $url) {
						echo 'iconURL.push("'.$url.'");';
					}
				?>
								
				// for each venue, create new marker and info window
				for (var i = 0; i < max; i++) {
					var marker = new google.maps.Marker( {
						position: new google.maps.LatLng(latArray[i], lngArray[i]), 
						map: map, 
						title: names[i],
						icon: iconURL[i]
					});
					venues.push(marker);
					// make infowindow content
					var contStr = names[i] + '<br>' +
									address[i] + '<br>' +
									latArray[i] + '<br>' +
									lngArray[i] + '<br>';
					var infoWindow = new google.maps.InfoWindow( {
						content: contStr
					});
					infoWindows.push(infoWindow);
					google.maps.event.addListener(venues[i], 'click', function(key) {
						return function() {
							infoWindows[key].open(map, venues[key]);
						}
					} (i) );
				}

			}

			function updateTextInput(val, id) {
				document.getElementById(id).value=val;
			}

			function formHandler() {
				if (newMarker == null) {
					alert("No query marker placed!");
					return false;
				} else {
					return true;
				}
			}

			google.maps.event.addDomListener(window, 'load', initialize);
		</script>
		<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDGDaBo1LuT9_wBfHiEZGqIf-q63XP9q5Q&amp;callback=initialize" async defer></script>
	</body>
</html>
