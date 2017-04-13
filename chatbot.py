# WRITTEN BY HYORIM KIM
# UNIVERSITY OF MICHIGAN
# APR 2017

import aiml
import os
import requests
import json
import time
import socket
CACHE_FNAME = 'cache.json'

#############################################
############# AIML KERNEL LOAD ##############
#############################################

kernel = aiml.Kernel()
kernel.verbose(False)
print "Hello there, please give me a second to load up."
kernel.learn(os.path.join('aiml_data', 'std-hello.aiml'))
for fil in os.listdir('aiml_data'):
	kernel.learn(os.path.join('aiml_data', fil))
print "All AIML_data loaded successfully. \nHello there, I am DarkSky Net."


#############################################
############# API CREDENTIALS ###############
#############################################

# Google Geocoding API Credentials
apik1 = "REPLACE YOUR API KEY HERE"
baseURL1 = "https://maps.googleapis.com/maps/api/geocode/json?"

# Dark Sky API Credentials
apik2 = "REPLACE YOUR API KEY HERE"
baseURL2 = "https://api.darksky.net/forecast/" + apik2 + "/"


#############################################
############## ATTEMPT CACHE ################
#############################################

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


#############################################
####### FETCH RESPONSE THROUGH CACHE ########
#############################################

# CACHE FUNCTION FOR GOOGLE GEOCODING API
def api1Cache(baseURL1, city):
	params = {
		'address': city,
		'key': apik1
	}
	req = requests.Request(method='GET', url=baseURL1, 
		params=sorted(params.items()))
	prepped = req.prepare()
	fullURL = prepped.url

	# Check to see if request exists in cache
	if fullURL not in CACHE_DICTION:
	# make the request and store the response
		response = requests.Session().send(prepped)
		CACHE_DICTION[fullURL] = response.text

	# Update cache file
	cache_file = open(CACHE_FNAME, 'w')
	cache_file.write(json.dumps(CACHE_DICTION))
	cache_file.close()

	# Return cache file
	return CACHE_DICTION[fullURL]

# CACHE FUNCTION FOR DARK SKY API
def api2Cache(baseURL2, dict):
	prepped = baseURL2 + str(dict['lat']) + ',' + str(dict['lng'])
	fullURL = prepped

	# Check to see if request exists in cache
	if fullURL not in CACHE_DICTION:
		response = requests.get(fullURL)
		CACHE_DICTION[fullURL] = response.text

	# Update cache file
	cache_file = open(CACHE_FNAME, 'w')
	cache_file.write(json.dumps(CACHE_DICTION))
	cache_file.close()

	# Return cache file
	return CACHE_DICTION[fullURL]


#############################################
####### KERNEL PROMPT LEARNING LIST #########
#############################################

# PROMPT: I live in {city}, {state}
def learn0(city, state):
    return '{}, eh? Do you like it in {}?'.format(state, city)
kernel.addPattern("i live in {city}, {state}", learn0)

# PROMPT: What's the weather like in {city}?
def learn1(city):
	if city == "FAKE CITY":
		return 'Is {city} a city?'.format(city=city)
	else:
		try:
			req = unwrapResponseAPI2(json.loads(api2Cache(baseURL2, 
				unwrapResponseAPI1(json.loads(api1Cache(baseURL1, city))))))
			return 'In {city}, it is {temp} and {cond}'.format(city= city, 
				temp=req['temp'], cond=req['current'])
		except:
			return errorHandler(city)
kernel.addPattern("what's the weather like in {city}?", learn1)

# PROMPT: Is it going to rain in {city} this week?
def learn2(city):
	if city == "FAKE CITY":
		return 'Is {city} a city?'.format(city=city)
	else:
		try:
			req = unwrapResponseAPI2(json.loads(api2Cache(baseURL2, 
				unwrapResponseAPI1(json.loads(api1Cache(baseURL1, city))))))
			return rainP(req['rainweek'], city)
		except:
			return errorHandler(city)
kernel.addPattern("is it going to rain in {city} this week?", learn2)

# PROMPT: Is it going to rain in {city} today?
def learn3(city):
	if city == "FAKE CITY":
		return 'Is {city} a city?'.format(city=city)
	else:
		try:
			req = unwrapResponseAPI2(json.loads(api2Cache(baseURL2, 
				unwrapResponseAPI1(json.loads(api1Cache(baseURL1, city))))))
			return rainP([req['rainprob']], city)
		except:
			return errorHandler(city)
kernel.addPattern("is it going to rain in {city} today?", learn3)

# PROMPT: How {hot/cold} will it get in {city} this week?
def learn4(condition, city):
	if city == "FAKE CITY":
		return 'Is {city} a city?'.format(city=city)
	else:
		try:
			req = unwrapResponseAPI2(json.loads(api2Cache(baseURL2, 
				unwrapResponseAPI1(json.loads(api1Cache(baseURL1, city))))))
		except:
			return errorHandler(city)

		if (condition == "hot") or (condition == "warm"):
			return 'In {city} it will reach {temp}'.format(city= city, 
				temp=max(req['maxweek']))
		elif condition == "cold":
			return 'In {city} it will reach {temp}'.format(city= city, 
				temp=min(req['minweek']))
		else:
			return 'I don\'t know what {condition} means.'.format(condition=condition)
kernel.addPattern("how {condition} will it get in {city} this week?", learn4)


#############################################
################ FUNCTIONS ##################
#############################################

# CHECK INTERNET CONNECTION
def checkInternet():
	try:
		# connected
		socket.create_connection(("www.google.com", 80))
		return True
	except:
		# no internet
		pass
	return False

# RESPONSE UNWRAPPER FOR GOOGLE GEOCODING API
def unwrapResponseAPI1(dict):
	# input:  returned json dict from makeRequestAPI1
	# return: dictionary of (status, lat, lng)

	return {'status':dict['status'], 
		'lat':dict['results'][0]['geometry']['location']['lat'], 
		'lng':dict['results'][0]['geometry']['location']['lng']}

# RESPONSE UNWRAPPER FOR DARK SKY API
def unwrapResponseAPI2(dict):
	# input:  returned json dict from makeRequestAPI2
	# return: dictionary of
	newdict = {}
	newdict['current'] = dict['currently']['summary']
	newdict['temp'] = dict['currently']['temperature']
	newdict['rainprob'] = dict['currently']['precipProbability']
	newdict['rainweek'] = []
	newdict['minweek'] = []
	newdict['maxweek'] = []
	for day in range(0, 8):
		newdict['rainweek'].append(dict['daily']['data'][day]['precipProbability'])
		newdict['minweek'].append(dict['daily']['data'][day]['temperatureMin'])
		newdict['maxweek'].append(dict['daily']['data'][day]['temperatureMax'])
	return newdict

# COMPUTE RAIN-PROBABILITY
def rainP(lst, city):
	# formula: 1 - ((prob it wont rain day 1)*(prob it wont rain day 2)...)
	# prob of raining for that day is ['daily']['data'][0]['precipProbability']
	# prob of raining for next day is len(requestStr['daily']['data'])
	minus = 1.0
	if len(lst) == 1:
		minus -= lst[0]
		prob = 1.0 - minus
	else:
		for i in range(0, len(lst)):
			minus *= (1.0-lst[i])
		prob = 1.0 - minus

	if prob < 0.1:
		return "It almost definitely will not rain in " + city
	elif prob > 0.1 and prob < 0.5:
		return "It probably will not rain in " + city
	elif prob > 0.5 and prob < 0.9:
		return "It probably will rain in " + city
	elif prob > 0.9:
		return "It will almost definitely rain in " + city
	else:
		return "There seems to be an error in calculating rain probability"


#############################################
######### ERROR HANDLING PROTOCOL ###########
#############################################

def errorHandler(city):
	print "is {city} a city?"


#############################################
############## MAIN FUNCTION ################
#############################################

ternet = False

while(True):
	user_input = raw_input("> ")
	if (checkInternet() != True):
		if ternet == False:
			ternet = True
			print ("DarkSky Net Lost Connection to Internet. \n All following prompts are cache-dependent until noted otherwise.")
	else:
		if ternet == True:
			ternet = False
			print ("DarkSky Net Regained Connection to Internet.")

	if user_input == "exit":
		print ("DarkSky Net Shutting Down. Good Bye.")
		break
	else:
		print(kernel.respond(user_input))
