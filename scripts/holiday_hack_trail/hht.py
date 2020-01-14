#======================================================================================================================
# Program: hht.py
#
# Description: Python client to play the SANS Holiday Hack Trail online game. Incorporates cheat codes!
#
# Date: 12/2019
#
# Author: deckerXL
#
# Examples:
#
# python3 hht.py --playerid=JebediahSpringfield --difficulty=hard --pace=2 --extrareindeer=1 --extrarunners=1
# --extrafood=5 --extrameds=2 --extraammo=5 --proxy --proxy_host=127.0.0.1 --proxy_port=8080
#
# python3 hht.py --playerid=JebediahSpringfield --difficulty=hard --pace=2 --extrareindeer=0 --extrarunners=0
# --extrafood=0 --extrameds=0 --extraammo=25 --invulnerability --proxy --proxy_host=127.0.0.1 --proxy_port=8080
#
# python3 hht.py --playerid=JebediahSpringfield --difficulty=easy --pace=2 --extrareindeer=0 --extrarunners=0
# --extrafood=10 --extrameds=10 --extraammo=20 --allmax --proxy --proxy_host=127.0.0.1 --proxy_port=8080
#
# Don't forget to check out all the CHEAT CODE options below!
#======================================================================================================================
import sys
import re
import random
import statistics
import argparse
import requests
requests.packages.urllib3.disable_warnings() 

parser = argparse.ArgumentParser()
parser.add_argument("--playerid", help="Set PlayerId to send to the server", required=True)
parser.add_argument("--difficulty", help="Set difficulty level {easy, medium, hard}", required=True)
parser.add_argument("--pace", help="Set pace level {0, 1, 2}", required=True)
parser.add_argument("--extrareindeer", help="Number of extra reindeer to buy {0-9}", required=True)
parser.add_argument("--extrarunners", help="Number of extra runners to buy {0-9}", required=True)
parser.add_argument("--extrafood", help="Amount of extra food to buy {0-1000}", required=True)
parser.add_argument("--extrameds", help="Amount of extra meds to buy {0-100}", required=True)
parser.add_argument("--extraammo", help="Amount of extra ammo to buy {0-100}", required=True)
parser.add_argument("--proxy", action="store_true", help="Use proxy - proxy host/port values are in the code")
parser.add_argument("--proxy_host", help="Set proxy host - set in conjunction with --proxy")
parser.add_argument("--proxy_port", help="Set proxy port - set in conjunction with --proxy")
parser.add_argument("--debug", action="store_true", help="Enable debugging output")
parser.add_argument("--invulnerability", action="store_true", help="!!!CHEAT CODES!!! - Activate Invulnerability")
parser.add_argument("--lightspeed", action="store_true", help="!!!CHEAT CODES!!! - Activate Lightspeed - only works in easy or medium mode")
parser.add_argument("--maxammo", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited Ammo - only works in easy or medium mode")
parser.add_argument("--maxmeds", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited Meds - only works in easy or medium mode")
parser.add_argument("--maxfood", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited Food - only works in easy or medium mode")
parser.add_argument("--maxreindeer", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited Reindeer - only works in easy or medium mode")
parser.add_argument("--maxrunners", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited Runners - only works in easy or medium mode")
parser.add_argument("--maxmoney", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited Money - only works in easy or medium mode")
parser.add_argument("--maxall", action="store_true", help="!!!CHEAT CODES!!! - Activate Unlimited ALL - only works in easy or medium mode")
args = parser.parse_args()

hhc_host            = "https://trail.elfu.org"
hhc_gameselect_url  = "https://trail.elfu.org/gameselect/"
hhc_store_url       = "https://trail.elfu.org/store/"
hhc_trail_url       = "https://trail.elfu.org/trail/"
max_distance        = 8000
river               = [ 'ferry', 'ford', 'caulk' ]
min_ferry_threshold = 150
pace_names          = [ 'Steady', 'Strenuous', 'Grueling' ]
difficulty_level    = [ 'Easy', 'Medium', 'Hard']

proxy_host = "127.0.0.1"
proxy_port = "8080"
if len(args.proxy_host) > 0:
	proxy_host = str(args.proxy_host)[0:15]
if len(args.proxy_port) > 0:
	proxy_port = str(args.proxy_port)[0:5]

playerid_arg      = str(args.playerid[0:25])
difficulty_arg    = re.sub("\W","",str(args.difficulty)[0:6].lower()).capitalize()
pace_arg          = int(re.sub("\D","",str(args.pace)))
extrareindeer_arg = int(re.sub("\D","",str(args.extrareindeer)))
extrarunners_arg  = int(re.sub("\D","",str(args.extrarunners)))
extrafood_arg     = int(re.sub("\D","",str(args.extrafood)))
extrameds_arg     = int(re.sub("\D","",str(args.extrameds)))
extraammo_arg     = int(re.sub("\D","",str(args.extraammo)))

player_id = playerid_arg
userser_name = playerid_arg

if pace_arg>=0 and pace_arg<=2:
	pace = str(pace_arg)
else:
	print ("\n*** ERROR: ["+str(pace_arg)+"] is not a valid pace setting - must be number between 0-2\n")
	sys.exit(1)

if extrareindeer_arg>=0 and extrareindeer_arg<=9:
	reindeerqty = str(extrareindeer_arg)
else:
	print ("\n*** ERROR: ["+str(extrareindeer_arg)+"] is not a valid extrareindeer setting - must be number between 0-9\n")
	sys.exit(1)

if extrarunners_arg>=0 and extrarunners_arg<=9:
	runnerqty = str(extrarunners_arg)
else:
	print ("\n*** ERROR: ["+str(extrarunners_arg)+"] is not a valid extrarunners setting - must be number between 0-9\n")
	sys.exit(1)

if extrafood_arg>=0 and extrafood_arg<=1000:
	foodqty = str(extrafood_arg)
else:
	print ("\n*** ERROR: ["+str(extrafood_arg)+"] is not a valid extrafood setting - must be number between 0-1000\n")
	sys.exit(1)

if extrameds_arg>=0 and extrameds_arg<=100:
	medsqty = str(extrameds_arg)
else:
	print ("\n*** ERROR: ["+str(extrameds_arg)+"] is not a valid extrameds setting - must be number between 0-100\n")
	sys.exit(1)

if extraammo_arg>=0 and extraammo_arg<=100:
	ammoqty = str(extraammo_arg)
else:
	print ("\n*** ERROR: ["+str(extraammo_arg)+"] is not a valid extraammo setting - must be number between 0-100\n")
	sys.exit(1)

if difficulty_arg == "Hard" and args.lightspeed:
	print ("\n*** ERROR: You cannot use lightspeed cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if difficulty_arg == "Hard" and args.maxall:
	print ("\n*** ERROR: You cannot use maxall cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if args.maxall:
	args.maxammo = args.maxfood = args.maxmeds = args.maxmoney = args.maxreindeer = args.maxrunners = True

if difficulty_arg == "Hard" and args.maxammo:
	print ("\n*** ERROR: You cannot use maxammo cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if difficulty_arg == "Hard" and args.maxmeds:
	print ("\n*** ERROR: You cannot use maxmeds cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if difficulty_arg == "Hard" and args.maxfood:
	print ("\n*** ERROR: You cannot use maxfood cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if difficulty_arg == "Hard" and args.maxreindeer:
	print ("\n*** ERROR: You cannot use maxreindeer cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if difficulty_arg == "Hard" and args.maxrunners:
	print ("\n*** ERROR: You cannot use maxrunners cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

if difficulty_arg == "Hard" and args.maxmoney:
	print ("\n*** ERROR: You cannot use maxmoney cheat code with 'hard' difficulty\n")
	parser.print_help()
	sys.exit(1)

# =====================================================================
# Proxy support - great for Burp!
# =====================================================================
if args.proxy:
	proxies = {
	 "http":  "http://"+proxy_host+":"+proxy_port,
	 "https": "http://"+proxy_host+":"+proxy_port
	}
else:
	proxies = {}

# =====================================================================
# Explicitly set all our headers for each page
# =====================================================================
gameselect_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Upgrade-Insecure-Requests': '1'
}

store_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': hhc_host,
	'Referer': hhc_gameselect_url,
	'Upgrade-Insecure-Requests': '1'
}

trail_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': hhc_host,
	'Referer': hhc_store_url,
	'Upgrade-Insecure-Requests': '1'
}

# =====================================================================
# Setup defaults which are dependant on difficultly level
# =====================================================================
if difficulty_arg == "Easy":
	difficulty  = "0"
	money       = "5000"
	distance    = "0"
	curmonth    = "7"
	curday      = "1"
	reindeer    = "2"
	runners     = "2"
	ammo        = "100"
	meds        = "20"
	food        = "400"
elif difficulty_arg == "Medium":
	difficulty  = "1"
	money       = "3000"
	distance    = "0"
	curmonth    = "8"
	curday      = "1"
	reindeer    = "2"
	runners     = "2"
	ammo        = "50"
	meds        = "10"
	food        = "200"
elif difficulty_arg == "Hard":
	difficulty  = "2"
	money       = "1500"
	distance    = "0"
	curmonth    = "9"
	curday      = "1"
	reindeer    = "2"
	runners     = "2"
	ammo        = "10"
	meds        = "2"
	food        = "100"
else:
	print ("\n*** ERROR: ["+difficulty_arg+"] is not a valid difficulty setting\n")
	parser.print_help()
	sys.exit(1)

# =====================================================================
# Setup other defaults - same for all difficulty levels
# =====================================================================
reindeerprice = "500"
runnerprice   = "200"
foodprice     = "5"
medsprice     = "50"
ammoprice     = "20"
submit        = "Buy"
action        = "go"
name0         = "Ruth"
health0       = "100"
cond0         = "0"
cause0        = ""
deathday0     = "0"
deathmonth0   = "0"
name1         = "Mildred"
health1       = "100"
cond1         = "0"
cause1        = ""
deathday1     = "0"
deathmonth1   = "0"
name2         = "Mathias"
health2       = "100"
cond2         = "0"
cause2        = ""
deathday2     = "0"
deathmonth2   = "0"
name3         = "John"
health3       = "100"
cond3         = "0"
cause3        = ""
deathday3     = "0"
deathmonth3   = "0"
hash          = "HASH"

# =====================================================================
# Finances Check
# =====================================================================
reindeercost = str(int(reindeerqty) * int(reindeerprice))
if int(reindeercost) <= int(money):
	money = str(int(money) - (int(reindeerqty) * int(reindeerprice)))
else:
	print ("\n*** ERROR: ["+str(reindeerqty)+"] extra reindeer at price ["+str(reindeerprice)+"] is ["+str(reindeercost)+"] which exceeds ["+str(money)+"] money remaining\n")
	sys.exit(1)

runnercost = str(int(runnerqty) * int(runnerprice))
if int(runnercost) <= int(money):
	money = str(int(money) - (int(runnerqty) * int(runnerprice)))
else:
	print ("\n*** ERROR: ["+str(runnerqty)+"] extra runners at price ["+str(runnerprice)+"] is ["+str(runnercost)+"] which exceeds ["+str(money)+"] money remaining\n")
	sys.exit(1)

foodcost = str(int(foodqty) * int(foodprice))
if int(foodcost) <= int(money):
	money = str(int(money) - (int(foodqty) * int(foodprice)))
else:
	print ("\n*** ERROR: ["+str(foodqty)+"] extra food at price ["+str(foodprice)+"] is ["+str(foodcost)+"] which exceeds ["+str(money)+"] money remaining\n")
	sys.exit(1)

medscost = str(int(medsqty) * int(medsprice))
if int(medscost) <= int(money):
	money = str(int(money) - (int(medsqty) * int(medsprice)))
else:
	print ("\n*** ERROR: ["+str(medsqty)+"] extra meds at price ["+str(medsprice)+"] is ["+str(medscost)+"] which exceeds ["+str(money)+"] money remaining\n")
	sys.exit(1)

ammocost = str(int(ammoqty) * int(ammoprice))
if int(ammocost) <= int(money):
	money = str(int(money) - (int(ammoqty) * int(ammoprice)))
else:
	print ("\n*** ERROR: ["+str(ammoqty)+"] extra ammo at price ["+str(ammoprice)+"] is ["+str(ammocost)+"] which exceeds ["+str(money)+"] money remaining\n")
	sys.exit(1)

# =====================================================================
# httpGet
# =====================================================================
def httpGet (url,p,h):
	try:
		r = requests.get(url,
				proxies=proxies,
				headers=h,
				params=p,
				verify=False
		)
	except Exception as e:
		print ("ERROR: HTTP Error Occurred: ["+str(e)+"]")
		sys.exit(1)
	return r

# =====================================================================
# httpPost
# =====================================================================
def httpPost (url,cookie,d,h):
	try:
		r = requests.post(url,
				proxies=proxies,
				headers=h,
				cookies=cookie,
				data=d,
				verify=False
		)
	except Exception as e:
		print ("ERROR: HTTP Error Occurred: ["+str(e)+"]")
		sys.exit(1)
	return r

# =====================================================================
# Extract Party Progress from HTTP Response
# =====================================================================
def get_party_progress(t):

	# Start with progress object. No good end sentinel, so jumping 400 characters
	start_sentinel  = '<table id="progress">'
	end_sentinel    = ''

	i1 = t.find(start_sentinel)+len(start_sentinel)
	i2 = i1+400
	status_section = t[i1:i2]

	status_section = status_section.replace('<b>',"")
	status_section = status_section.replace('</b>',"|")
	status_section = status_section.replace('<tr>',"")
	status_section = status_section.replace('</tr>',"|")
	status_section = status_section.replace('<td>',"|")  # Missing close tag is forcing this asymmetry
	status_section = status_section.replace('</td>',"|")
	status_section = status_section.replace('<option>',"")
	status_section = status_section.replace('</option>',"|")
	status_section = status_section.replace('<select>',"")
	status_section = status_section.replace('</select>',"|")

	status_section = re.sub(r'\s+',' ',status_section)
	status_section = re.sub(r'\|\s+','|',status_section)
	status_section = re.sub(r'\s+\|','|',status_section)
	status_section = re.sub(r'\|+','|',status_section)

	status_section = re.sub('<select name="pace" class="pace">','', status_section)
	status_section = re.sub('</table> <!-- <table id="displayWindow" class="noborder">','', status_section)
	status_section = re.sub('<option value="0">Steady','', status_section)
	status_section = re.sub('<option value="1">Strenuous','', status_section)
	status_section = re.sub('<option value="2">Grueling','', status_section)
	status_section = re.sub(r'<option value="." selected>','', status_section)

	status_section = status_section.strip()
	status_section = re.sub(r'^\|+','',status_section)
	status_section = re.sub(r'\|+$','',status_section)

	if args.debug:
		print ("Status Section: ["+status_section+"]")

	return status_section

# =====================================================================
# Extract Status Container from HTTP Response
# =====================================================================
def get_status_container(t):

	# Get statusContainer object
	start_sentinel  = '<div id="statusContainer">'
	end_sentinel    = '<footer id="footer"></footer>'

	i1 = t.find(start_sentinel)+len(start_sentinel)
	i2 = t.find(end_sentinel)
	status_container = t[i1:i2]

	status_container = status_container.replace('<div>',"")
	status_container = status_container.replace('</div>',"|")
	status_container = status_container.replace('<form>',"")
	status_container = status_container.replace('</form>',"|")
	status_container = status_container.replace('<br>',"")
	status_container = status_container.replace('</br>',"|")

	status_container = status_container.replace('    <input type="hidden" name="','')
	status_container = re.sub('" class=".*" value="','|',status_container)
	status_container = re.sub('">','|',status_container)

	status_container = status_container.replace("\n","")

	status_container = status_container.strip()
	status_container = re.sub(r'^\|+','',status_container)
	status_container = re.sub(r'\|+$','',status_container)

	# Fix rare bug where server decremented reindeer value to negative number - reset negative to 0
	status_container = re.sub(r'reindeer\|-\d+\|','reindeer|0|',status_container)
	status_container = re.sub(r'runners\|-\d+\|','runners|0|',status_container)

	if args.debug:
		print ("Status Container: ["+status_container+"]")

	return status_container

# =====================================================================
# Extract Status Messages from HTTP Response
# =====================================================================
def get_status_messages(t):

	# Start with inventory table object
	start_sentinel  = '<table id="inventory"'
	end_sentinel    = '<footer id="footer"></footer>'

	i1 = t.find(start_sentinel)+len(start_sentinel)
	i2 = t.find(end_sentinel)
	status_messages = t[i1:i2]
	
	# No need to parse inventory table since this data is already obtained from the statusContainer, so skipping below it
	start_sentinel  = '</td></tr></table>'
	i1 = status_messages.find(start_sentinel)+len(start_sentinel)
	status_messages = status_messages[i1:]

	status_messages = status_messages.replace('<b>',"")
	status_messages = status_messages.replace('</b>',"|")
	status_messages = status_messages.replace('<br>',"")
	status_messages = status_messages.replace('</br>',"|")
	status_messages = status_messages.replace('<p>',"")
	status_messages = status_messages.replace('</p>',"|")
	status_messages = status_messages.replace('<div>',"")
	status_messages = status_messages.replace('</div>',"|")

	status_messages = status_messages.replace('(The overall distance remaining is shown in the top-left.)',' ')

	if args.invulnerability:
		status_messages = status_messages.replace('You have no food. Your party is starving.',' ')

	status_messages = re.sub(r'\s+',' ',status_messages)
	status_messages = re.sub(r'\|\s+','|',status_messages)
	status_messages = re.sub(r'\s+\|','|',status_messages)
	status_messages = re.sub(r'\|+','|',status_messages)

	status_messages = status_messages.strip()
	status_messages = re.sub(r'^\|+','',status_messages)
	status_messages = re.sub(r'\|+$','',status_messages)
	
	if args.debug:
		print ("Status Messages: ["+status_messages+"]")

	return status_messages

# =====================================================================
# Extract Trade Offer Details from HTTP Response
# =====================================================================
def get_trade_offer(t):

	# Start with inventory table object
	start_sentinel  = 'If you accept the trade, click Trade.  Anything else will cancel.'
	end_sentinel    = ''

	i1 = t.find(start_sentinel)+len(start_sentinel)
	i2 = i1+300
	trade_offer = t[i1:i2]

	trade_offer = re.sub(r'\s+',' ',trade_offer)
	trade_offer = trade_offer.replace('<br>',"")
	trade_offer = trade_offer.replace('</br>',"|")

	trade_offer = trade_offer.replace('<input type="hidden" name="','|')
	trade_offer = trade_offer.replace('" value=', '|')
	trade_offer = trade_offer.replace('> |', '|')
	trade_offer = re.sub(r'>.*','',trade_offer)

	trade_offer = trade_offer.strip()
	trade_offer = re.sub(r'^\|+','',trade_offer)
	trade_offer = re.sub(r'\|+$','',trade_offer)

	return trade_offer

# =====================================================================
# Extract JOURNEY END Data from Victory Page
# =====================================================================
def get_journeyend_data(t):

	# Start with the page container object
	start_sentinel = '<div id="page-container"><p>'
	end_sentinel   = '<footer id="footer"></footer>'

	i1 = t.find(start_sentinel)+len(start_sentinel)
	i2 = t.find(end_sentinel)
	
	journeyend_section = t[i1:i2]
	journeyend_section = journeyend_section.replace("\n","")
	journeyend_section = journeyend_section.replace('<p>',"")
	journeyend_section = journeyend_section.replace('</p>',"|")
	journeyend_section = journeyend_section.replace('<li>',"")
	journeyend_section = journeyend_section.replace('</li>',"|")
	journeyend_section = journeyend_section.replace('<ul>',"")
	journeyend_section = journeyend_section.replace('</ul>',"|")
	journeyend_section = journeyend_section.replace('<font color="#038ea5">',"|")
	journeyend_section = journeyend_section.replace('<font color="#9ea022">',"|")
	journeyend_section = journeyend_section.replace('<b>',"")
	journeyend_section = journeyend_section.replace('</b>',"|")
	journeyend_section = journeyend_section.replace('<script>',"")
	journeyend_section = journeyend_section.replace('</script>',"|")
	journeyend_section = journeyend_section.replace('<a>',"")
	journeyend_section = journeyend_section.replace('</a>',"|")
	journeyend_section = journeyend_section.replace('<div>',"")
	journeyend_section = journeyend_section.replace('</div>',"|")
	journeyend_section = journeyend_section.replace('<br>',"")
	journeyend_section = journeyend_section.replace('</br>',"|")
	journeyend_section = journeyend_section.replace('<font>',"")
	journeyend_section = journeyend_section.replace('</font>',"")

	journeyend_section = journeyend_section.replace('<script src="/conduit.js">',"")
	journeyend_section = journeyend_section.replace('<img src="art/pieces/header.png" alt="header">',"")
	journeyend_section = journeyend_section.replace('<ul style=\'list-style-type: none; padding: 0px; text-align: left;\'>',"")
	journeyend_section = journeyend_section.replace('<a href=\'/\'>',"")
	journeyend_section = journeyend_section.replace('Start over?',"")

	journeyend_section = re.sub(r'\s+',' ',journeyend_section)
	journeyend_section = re.sub(r'\|\s+','|',journeyend_section)
	journeyend_section = re.sub(r'\s+\|','|',journeyend_section)
	journeyend_section = re.sub(r'\|+','|',journeyend_section)

	journeyend_section = journeyend_section[:-1].strip()

	return journeyend_section

# =====================================================================
# Print Status
# =====================================================================
def print_status(sc,sm,a,p,tf):

	if a == "trade": a = a+"="+tf

	difficulty_stat = difficulty_level[int(sc[1])]
	action_stat		= a.upper().rjust(14)
	pace_stat		= p.upper().rjust(8)
	remaining_stat	= "Dist/Left:"+str('{:04}'.format(int(sc[5])))+"/"+str('{:04}'.format(max_distance-int(sc[5])))
	gamedate_stat	= "Date:"+str('{:02}'.format(int(sc[7])))+"/"+str('{:02}'.format(int(str(sc[9]))))
	money_stat		= "Money:"+str('{:04}'.format(int(sc[3])))
	reindeer_stat	= "Reindr:"+str('{:02}'.format(int(sc[59])))
	runners_stat	= "Runrs:"+str('{:02}'.format(int(sc[61])))
	ammo_stat		= "Ammo:"+str('{:03}'.format(int(sc[63])))
	meds_stat		= "Meds:"+str('{:03}'.format(int(sc[65])))
	food_stat		= "Food:"+str('{:03}'.format(int(sc[67])))
	health_stat		= "Heath:"+str('{:03}'.format(int(sc[13])))+"/"+str('{:03}'.format(int(sc[25])))+"/"+\
						 str('{:03}'.format(int(sc[37])))+"/"+str('{:03}'.format(int(sc[49])))

	print ("STATUS - ["+action_stat+"] ["+difficulty_stat+"] ["+pace_stat+"] ["+remaining_stat+"] ["+gamedate_stat+"] ["+
		   money_stat+"] ["+reindeer_stat+"] ["+runners_stat+"] ["+ammo_stat+"] ["+meds_stat+"] ["+food_stat+"] ["+health_stat+"]")

	if len(sm) == 0:
		sm = "No Updates"
	print ("\t ["+sm+"]\n")

# =====================================================================
# Attempt very simple decision logic to help our friends on the trail
# This is life favoring logic
# =====================================================================
def next_action_logic(sc,a,p):

	difficulty_stat = str(sc[1])
	distance_stat   = str(sc[5])
	curmonth_stat   = str(sc[7])
	ammo_stat       = str(sc[63])
	meds_stat       = str(sc[65])
	food_stat       = str(sc[67])
	reindeer_stat   = str(sc[59])
	runners_stat    = str(sc[61])
	health0_stat    = str(sc[13])
	health0_cond    = str(sc[15])
	health1_stat    = str(sc[25])
	health1_cond    = str(sc[27])
	health2_stat    = str(sc[37])
	health2_cond    = str(sc[39])
	health3_stat    = str(sc[49])
	health3_cond    = str(sc[51])

	health_average = 0
	party_members  = 4
	home_stretch   = 7500

	if int(health0_cond)<0: party_members = party_members-1
	if int(health1_cond)<0: party_members = party_members-1
	if int(health2_cond)<0: party_members = party_members-1
	if int(health3_cond)<0: party_members = party_members-1
	if party_members>0:
		health_average = round((int(health0_stat)+int(health1_stat)+int(health2_stat)+int(health3_stat))/party_members)

	health_stat_set = [ int(health0_stat), int(health1_stat), int(health2_stat), int(health3_stat),]
	health_median = statistics.median(health_stat_set)
	
	new_action   = a
	new_pace     = p 

	urgent_resources    = 10
	critical_health     = 30
	moderate_health     = 50
	urgent_health       = 15
	new_tradefor	    = ""

	important_resources1 = ['Food','Ammo']
	important_resources2 = ['Food','Meds']

	if int(runners_stat) < 2:
		new_action = "trade"
		new_tradefor = "Runners"
	elif int(reindeer_stat) < 1:
		new_action = "trade"
		new_tradefor = "Reindeer"
	else:
		if int(food_stat) < urgent_resources: #and health_average < critical_health:
			if int(ammo_stat) > 0:
				new_action = "hunt"
			else:
				if health_average < urgent_health:
					if difficulty_stat == 2 and distance_stat <= home_stretch:  # If on hard and almost there, just go
						new_action = "go"
					else:
						new_action = "trade"
						#Randomly choose in this case between Food or Ammo as next trade
						toss_up = random.randint(0,1)
						new_tradefor = important_resources1[toss_up]

		if not new_action == "hunt":
			if (
				(int(health0_stat)<urgent_health and int(health0_cond)>=0) or
				(int(health1_stat)<urgent_health and int(health1_cond)>=0) or
				(int(health2_stat)<urgent_health and int(health2_cond)>=0) or
				(int(health3_stat)<urgent_health and int(health3_cond)>=0)
			):
				if int(meds_stat) > 0:
					new_action = "meds"
				else:
					if difficulty_stat == 2 and distance_stat <= home_stretch:  # If on hard and almost there, just go
						new_action = "go"
					else:
						new_action = "trade"
						# Randomly choose in this case between Food or Meds as next trade
						toss_up = random.randint(0,1)
						new_tradefor = important_resources2[toss_up]

	# Downgrade Pace if Health urgent
	if int(food_stat) == 0 and health_average < urgent_health:
		if int(new_pace) == 2:
			new_pace = "1"
		elif int(new_pace) == 1:
			new_pace = "0"

	# Upgrade Pace if Health improved
	if health_average >= moderate_health:
		if int(new_pace) == 0:
			new_pace = "1"
		elif int(new_pace) == 1:
			new_pace = "2"

	return new_action, new_pace, new_tradefor

# =====================================================================
# Analyze Trade Offer
# =====================================================================
def trade_offer_logic(o,sc):

	decision = False

	offer_itemQty       = o[1]
	offer_tradeFor      = o[3]
	offer_reqQty        = o[5]
	offer_itemRequested = o[7]

	min_runners     = 2
	min_reindeer    = 2
	acceptable_loss = 0.5

	if args.debug:
		print ("ANALYSIS: ["+offer_itemQty+"] ["+offer_tradeFor+"] ["+offer_reqQty+"] ["+offer_itemRequested+"]")

	if offer_tradeFor == "Runners":
		acceptable_loss = 1
		min_reindeer    = 1

	if offer_itemRequested == "Money":
		if int(offer_reqQty) <= int(sc[3]):
			decision = True
			if args.debug:
				print("TRADING: Will Trade for Money!")
	elif offer_itemRequested == "Ammo":
		if int(offer_reqQty) <= int(int(sc[63]) * acceptable_loss):
			decision = True
			if args.debug:
				print("TRADING: Will Trade for Ammo!")
	elif offer_itemRequested == "Meds":
		if int(offer_reqQty) <= int(int(sc[65]) * acceptable_loss):
			decision = True
			if args.debug:
				print ("TRADING: Will Trade for Meds!")
	elif offer_itemRequested == "Food":
		if int(offer_reqQty) <= int(int(sc[67]) * acceptable_loss):
			decision = True
			if args.debug:
				print ("TRADING: Will Trade for Food!")
	elif offer_itemRequested == "Reindeer":
		if int(offer_reqQty) < int(sc[59]) and int(sc[59]) > min_reindeer:
			decision = True
			if args.debug:
				print ("TRADING: Will Trade for Reindeer!")
	elif offer_itemRequested == "Runners":
		if int(offer_reqQty) < int(sc[61]) and int(sc[61]) > min_runners:
			decision = True
			if args.debug:
				print ("TRADING: Will Trade for Runners!")

	return decision

# =====================================================================
# =====================================================================
# ### MAIN
# =====================================================================
# =====================================================================

# Display user input game options
print ("\nGAME OPTIONS: Difficulty:["+difficulty_arg+"] - Pace:["+pace_names[pace_arg]+"] - ExtraReindeer:["+reindeerqty+"] - ExtraRunners:["+runnerqty+"] - ExtraFood:["+foodqty+"] - Extrameds:["+medsqty+"] - Extaammo:["+ammoqty+"]")

cheat_codes_active = ""
if args.lightspeed:
	cheat_codes_active = cheat_codes_active + "lightspeed "
if args.maxammo:
	cheat_codes_active = cheat_codes_active + "maxammo "
if args.maxmeds:
	cheat_codes_active = cheat_codes_active + "maxmeds "
if args.maxfood:
	cheat_codes_active = cheat_codes_active + "maxfood "
if args.maxreindeer:
	cheat_codes_active = cheat_codes_active + "maxreindeer "
if args.maxrunners:
	cheat_codes_active = cheat_codes_active + "maxrunners "
if args.maxmoney:
	cheat_codes_active = cheat_codes_active + "maxmoney "
if args.invulnerability:
	cheat_codes_active = cheat_codes_active + "invulnerability "

cheat_codes_active = cheat_codes_active.strip()

if cheat_codes_active == "":
	cheat_codes_active = "none"

print ("              !!!! CHEAT CODES ACTIVE: ["+cheat_codes_active+"]")
print ("")

#-----------------------------------
# GET gameselect URL
#-----------------------------------
get_params = {
	'playerid': player_id,
	'username': userser_name
}
get_response = httpGet(hhc_gameselect_url,get_params,gameselect_headers)
returned_cookie = get_response.cookies['trail-mix-cookie']

#-----------------------------------
# POST to store URL
#-----------------------------------
store_data_init = {
		'difficulty': difficulty_arg,
		'playerid': player_id,
		'username': userser_name
}

cookie_data = {
        'trail-mix-cookie': returned_cookie
}
post_response = httpPost(hhc_store_url,cookie_data,store_data_init,store_headers)
returned_cookie = post_response.cookies['trail-mix-cookie']

status_container = get_status_container(post_response.text).split('|')
money       = str(status_container[3])
distance    = str(status_container[5])
curmonth    = str(status_container[7])
curday      = str(status_container[9])
name0       = str(status_container[11])
name1       = str(status_container[23])
name2       = str(status_container[35])
name3       = str(status_container[47])
reindeer    = str(status_container[59])
runners     = str(status_container[61])
ammo        = str(status_container[63])
meds        = str(status_container[65])
food        = str(status_container[67])
hash        = str(status_container[69])

if not args.invulnerability:
	health0     = str(status_container[13]) 
	cond0       = str(status_container[15]) 
	cause0      = str(status_container[17]) 
	deathday0   = str(status_container[19]) 
	deathmonth0 = str(status_container[21])
	health1     = str(status_container[25]) 
	cond1       = str(status_container[27]) 
	cause1      = str(status_container[29]) 
	deathday1   = str(status_container[31]) 
	deathmonth1 = str(status_container[33])
	health2     = str(status_container[37]) 
	cond2       = str(status_container[39]) 
	cause2      = str(status_container[41]) 
	deathday2   = str(status_container[43]) 
	deathmonth2 = str(status_container[45])
	health3     = str(status_container[49]) 
	cond3       = str(status_container[51]) 
	cause3      = str(status_container[53]) 
	deathday3   = str(status_container[55]) 
	deathmonth3 = str(status_container[57])

if args.debug:
	print ("============================================================")
	print (post_response.headers)
	print ("============================================================")
	print (post_response.content)
	print ("============================================================")
	print ("Cookied Returned: "+returned_cookie)

store_post_pending = True

#-----------------------------------
# POST to trail recurring URL
#-----------------------------------
journey_end = False
while not journey_end:

	trail_list  = 	[
		"playerid="+player_id,
		"difficulty="+difficulty,
		"money="+money,
		"distance="+distance,
		"curmonth="+curmonth,
		"curday="+curday,
		"name0="+name0,
		"health0="+health0,
		"cond0="+cond0,
		"cause0="+cause0,
		"deathday0="+deathday0,
		"deathmonth0="+deathmonth0,
		"name1="+name1,
		"health1="+health1,
		"cond1="+cond1,
		"cause1="+cause1,
		"deathday1="+deathday1,
		"deathmonth1="+deathmonth1,
		"name2="+name2,
		"health2="+health2,
		"cond2="+cond2,
		"cause2="+cause2,
		"deathday2="+deathday2,
		"deathmonth2="+deathmonth2,
		"name3="+name3,
		"health3="+health3,
		"cond3="+cond3,
		"cause3="+cause3,
		"deathday3="+deathday3,
		"deathmonth3="+deathmonth3,
		"reindeer="+reindeer,
		"runners="+runners,
		"ammo="+ammo,
		"meds="+meds,
		"food="+food,
		"hash="+hash
		]

	# -----------------------------------
	# Set additional POST variables
	# -----------------------------------
	if store_post_pending:
		trail_list.insert(0,"reindeerqty="+reindeerqty)
		trail_list.insert(1,"runnerqty="+runnerqty)
		trail_list.insert(2,"foodqty="+foodqty)
		trail_list.insert(3,"medsqty="+medsqty)
		trail_list.insert(4,"ammoqty="+ammoqty)
		trail_list.insert(5,"submit="+submit)
		store_post_pending = False
	else:
		if action == "trade":
			if len(trade_offer) > 0:
				make_trade = trade_offer_logic(trade_offer,status_container)
				if not make_trade:
					action = "trade"
					trail_list.insert(1, "tradeFor=" + tradeFor)
				else:
					trail_list.insert(1, trade_offer[0]+"="+trade_offer[1])
					trail_list.insert(2, trade_offer[2]+"="+trade_offer[3])
					trail_list.insert(3, trade_offer[4]+"="+trade_offer[5])
					trail_list.insert(4, trade_offer[6]+"="+trade_offer[7])
			else:
				trail_list.insert(1, "tradeFor=" + tradeFor)
		trail_list.insert(0,"pace=" + pace)
		trail_list.insert(2,"action=" + action)

	trail_data = ""
	for i in range (0,len(trail_list)):
		trail_data = trail_data + trail_list[i]+"&"
	trail_data = trail_data[:-1]

	cookie_data = {
		'trail-mix-cookie': returned_cookie
	}
	post_response = httpPost(hhc_trail_url,cookie_data,trail_data,trail_headers)

	if post_response.text.find('502 Bad Gateway')>0:
		print ("ERROR: HTTP 502 Bad Gateway")
		sys.exit(1)

	if post_response.text.find('Your party has succeeded!')>0:
		journey_end = True
		journeyend_data = get_journeyend_data(post_response.text)
		print ("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("!!! VICTORY !!!: ["+journeyend_data+"]")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
	elif post_response.text.find('Your party has failed because everyone\'s dead.')>0:
		journey_end = True
		journeyend_data = get_journeyend_data(post_response.text)
		print ("\n==================================================================")
		print ("FAILED: ["+journeyend_data+"]")
		print ("==================================================================\n")
	elif post_response.text.find('Your party has failed because you ran out of time.')>0:
		journey_end = True
		journeyend_data = get_journeyend_data(post_response.text)
		print ("\n==================================================================")
		print ("FAILED: ["+journeyend_data+"]")
		print ("==================================================================\n")
	else:
		status_container    = get_status_container(post_response.text).split('|')
		status_messages     = get_status_messages(post_response.text)

		trade_offer = ""
		if post_response.text.find('If you accept the trade, click Trade') > 0:
			trade_offer = get_trade_offer(post_response.text).split('|')

		if post_response.text.find('Your sleigh has fewer than two runners. You did not progress.') > 0:
			print ("BADNEWS: Your sleigh has fewer than two runners. You did not progress.")
		if post_response.text.find('Oh dear! One of your reindeer has vanished.') > 0:
			print ("BADNEWS: Oh dear! One of your reindeer has vanished.")
		if post_response.text.find('Oh no! One of your sleigh\'s runners has broken.') > 0:
			print ("BADNEWS: Oh no! One of your sleigh's runners has broken.")
		if post_response.text.find('has died.') > 0:
			print ("BADNEWS: One of your party members has died!")
		if post_response.text.find('You managed to tame a wild reindeer!') > 0:
			print ("GOODNEWS:You managed to tame a wild reindeer!")
		if post_response.text.find('You found a spare runner lying on the ground!') > 0:
			print ("GOODNEWS:You found a spare runner lying on the ground!")

		money    = str(status_container[3])

		# River Crossing Logic
		crossing_river = False
		if (post_response.text.find('>Ferry<')>0) and (post_response.text.find('>Ford<')>0) and (post_response.text.find('>Caulk<')>0):
			if int(money) >= min_ferry_threshold:
				choice = 0  # If you have sufficient money, then Ferry as safest option
			else:
				choice = random.randint(1,2)  # Don't allow Ferry as an option if not enough money
			action = str(river[choice])
			print ("RIVER CROSSING CHOICE - You choose to: ["+action.capitalize()+"]")
			crossing_river = True
		else:
			action = "go"

		distance = str(status_container[5])
		curmonth = str(status_container[7])
		curday   = str(status_container[9])
		name0    = str(status_container[11])
		name1    = str(status_container[23])
		name2    = str(status_container[35])
		name3    = str(status_container[47])
		reindeer = str(status_container[59])
		runners  = str(status_container[61])
		ammo     = str(status_container[63])
		meds     = str(status_container[65])
		food     = str(status_container[67])
		hash     = str(status_container[69])

		if not args.invulnerability:
			health0     = str(status_container[13]) 
			cond0       = str(status_container[15]) 
			cause0      = str(status_container[17]) 
			deathday0   = str(status_container[19]) 
			deathmonth0 = str(status_container[21])
			health1     = str(status_container[25]) 
			cond1       = str(status_container[27]) 
			cause1      = str(status_container[29]) 
			deathday1   = str(status_container[31]) 
			deathmonth1 = str(status_container[33])
			health2     = str(status_container[37]) 
			cond2       = str(status_container[39]) 
			cause2      = str(status_container[41])
			deathday2   = str(status_container[43]) 
			deathmonth2 = str(status_container[45])
			health3     = str(status_container[49]) 
			cond3       = str(status_container[51]) 
			cause3      = str(status_container[53]) 
			deathday3   = str(status_container[55]) 
			deathmonth3 = str(status_container[57])

		if int(difficulty)<2:
			if args.lightspeed:
				lightspeed = random.randint(500,1000)
				distance = status_container[5] = str(int(distance)+lightspeed)
				if args.debug:
					print ("CHEAT CODE - TRAVELING LIGHTSPEED!!!... Distance Jump:["+str(lightspeed)+"]")
			if args.maxammo:
				ammo = status_container[63] = "999"
				if args.debug:
					print ("CHEAT CODE - MAX AMMO!!!...:["+str(maxammo)+"]")
			if args.maxmeds:
				meds = status_container[65] = "999"
				if args.debug:
					print ("CHEAT CODE - MAX MEDS!!!...:["+str(maxmeds)+"]")
			if args.maxfood:
				food = status_container[67] = "9999"
				if args.debug:
					print ("CHEAT CODE - MAX FOOD!!!...:["+str(maxfood)+"]")
			if args.maxreindeer:
				reindeer = status_container[59] = "99"
				if args.debug:
					print ("CHEAT CODE - MAX REINDEER!!!...:["+str(maxreindeer)+"]")
			if args.maxrunners:
				runners = status_container[61] = "99"
				if args.debug:
					print ("CHEAT CODE - MAX RUNNERS!!!...:["+str(maxrunners)+"]")
			if args.maxmoney:
				money = status_container[3] = "9999"
				if args.debug:
					print ("CHEAT CODE - MAX MONEY!!!...:["+str(maxmoney)+"]")

		# ==========================================
		# Extremely simple AI
		# ==========================================
		tradeFor = ""
		if not crossing_river:
			(action,pace,tradeFor) = next_action_logic(status_container,action,pace)

		# ==========================================
		# Print Status
		# ==========================================
		print_status(status_container,status_messages,action,pace_names[int(pace)],tradeFor)

		returned_cookie = post_response.cookies['trail-mix-cookie']
		party_progress_data = get_party_progress(post_response.text).split('|')

		if args.debug:
			print ("Party Progress Data: ["+str(party_progress_data)+"]")

		del trail_list[:]

sys.exit(0)
