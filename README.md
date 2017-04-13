# pyaiml_chatbot
Simple python AIML chatbot for basic weather information.

# MOTIVATION:
	This chatbot.py was created for the purpose of a course
	final project for SI 106 at the University of Michigan.
	We were given the boilerplate aiml to build upon our 'bot'.
	Please refer to the 'spec.pdf' file for project specifications.


# CAPABILITIES:
	Chatbot.py is able to respond to the following prompts (case non-sensitive): <br>
	- 'What's the weather like in {city}?' <br>
	- 'Is it going to rain in {city} this week?' <br>
	- 'How {hot/cold} will it get in {city} this week?' <br>
	- 'Is it going to rain in {city} today?' <br>

	While running, Chatbot will notify you when an internet
	connection has been compromised. When your device loses
	internet connection, it will tell you that all prompts
	thereafter will depend solely on cached responses.


# DEPENDENCIES:
	Chatbot.py is built on Python 2.7!
	Chatbot.py imports aiml, os, requests, json, time, socket,
	and a locally set 'cache.json' file.
	It utilizes a GET request call to Google Geocoding API
	to capture city geocodes and Dark Sky API to capture
	weather data.
	The utilized AIML files were modified by the Faculty and
	Staff at the School of Information of SI106.


## GOOGLE GEOCIDING API:
	Standard calls with a sample full request URL:
	'https://maps.googleapis.com/maps/api/geocode/json?address=[street_address],+[city],+[state]&key=[APIK]'


## DARK SKY API:
	Dark Sky's API calls are slightly cumbersom in that the
	URL's must be manually modified to get the responses.
	Standard calls with a sample full request URL:
	'https://api.darksky.net/forecast/[APIK]/[latitude],[longitude]'


# INSTRUCTIONS:
	Simply fork and/or download the repo and run Terminal.
	If zipped, unzip it and travel to the folder location.
	for example you can type in Terminal, "cd ~/Desktop"

	On any text editor of your choice, open up 'chatbot.py'
	replace the 'apik1' and 'apik2' values as per your own API Keys
	for both API services.

	For an API for Google, you must have a Google account, then
	go to "https://console.developers.google.com" and activate the
	Geocoding API on your account, then register for an API Key.

	You can register for a Dark Sky account for the API Key here:
	"https://darksky.net/dev/register"


	Once within the project folder, type in Terminal,
	"python chatbot.py" to start Chatbot.py

	Calculating Rain Probabilities:
	- There is a section on this calculation on the 'spec.pdf'
