#check Version Coded by dogo h@ck(MGF15)

import sys, urllib2, re, os , colorama , urllib

from colorama import Fore, Back, Style , init

colorama.init()
	
Dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
site=open(Dir +'OUT','r')
dogo=open(Dir +'Found.txt','r')
host=site.readline()
print host
for exploit in dogo.read().split('\n'):
	try:
		resp = (host + '/wp-content/plugins/' + exploit + '/readme.txt')
		F	 =	urllib2.urlopen(resp)
		B=F.read()
		v=re.findall(r'(Stable tag: \w+.\w+)',B)
		n=re.findall(r'(Stable tag: \w+.\w+.\w+)',B)
		if n:
			print (Fore.GREEN + "\n\t"), exploit , (Fore.YELLOW + "===>"),n[0]
		elif v:
			print (Fore.GREEN + "\n\t"), exploit , (Fore.YELLOW + "===>"),v[0]

	except:
		pass
