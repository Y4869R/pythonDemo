'''
dis: adb command
date: 2019-09-30
author: mlgc4869
'''

import os
import sys
import json

################################# global variable ##################################
configPath = r"C:\Users\chendh\Desktop\srafconfig.json"

adbDisconnect = 'adb disconnect '
adbConnect = 'adb connect '
adbRoot = "adb root "
adbRemount = 'adb remount '
adbPush = 'adb push '
adbSetting = 'adb shell settings '
adbReboot = 'adb reboot '

setProxycmd = 'adb shell settings put global http_proxy '
srcLibPath = ''
proxy = ''
sysLibPath = ''

DEBUG = False
################################# global variable ##################################


########################### enum ProxyOperation ####################################
class ProxyOperation:
	GET = 1
	SET = 2
	DEL = 3
########################### enum ProxyOperation ####################################


########################### function controlProxy ##################################
def controlProxy(operation, proxy):
	if operation == ProxyOperation.GET:
		result = executeCmd(adbSetting + ' get global http_proxy ' )
		if len(result) != 0:
			clearScreen()
			print('######[INFO]: get proxy :' + result[0])
	elif operation == ProxyOperation.SET:
		result = executeCmd(adbSetting + ' put global http_proxy ' + proxy)
		print('######[INFO]: set proxy done!')
	elif operation == ProxyOperation.DEL:
		result = executeCmd(adbSetting + ' delete global http_proxy')
		result += executeCmd(adbSetting + ' delete global global_http_proxy_host')
		result += executeCmd(adbSetting + ' delete global global_http_proxy_port')
		print('######[INFO]: delete proxy done!')

	return result
########################### function controlProxy ##################################


########################### function clearScreen ####################################
def clearScreen():
	os.system('cls')
########################### function clearScreen ####################################


########################### function executeCmd ######################################
def executeCmd(cmd):
	if len(cmd) == 0:
		print('######[ERROR]: cmd is empty #####')
		return ''
	else:
		if DEBUG:
			print('######[DEBUG]:  ' + cmd + ' start #####')
		result = os.popen(cmd).readlines()
		if DEBUG:
			print(result)
			print('######[DEBUG]:  ' + cmd + ' end #####')
		return result
########################### function executeCmd ######################################

########################### function cpLib ######################################
def cpLib(srcpath, targetpath):
	if DEBUG:
		print("srcpath:" +srcpath + " , targetpath:" + targetpath)
	if len(srcpath)==0 or len(targetpath)==0:
		print('######[ERROR]: path is empty #####')
		return
	cmd = adbPush + ' ' + srcpath + '\\.  ' + targetpath
	print('######[INFO]: copying lib from ' + srcpath +' to ' + targetpath +' #####')
	result = executeCmd(cmd)
	if len(result):
		clearScreen()
		print result[0]
		print('######[INFO]: cp lib to ' + targetpath +' done #####')
########################### function cpLib ######################################


########################### function action ######################################
def action():
	print('**************************')
	print('1.copy lib')
	print('2.proxy operation')
	print('3.apk operation')
	print('4.logcat')
	print('5.refresh configs')
	print('6.reboot')
	print('0.exit')
	print('**************************')
	print("Please Enter your chioce:")
	choice = str(input())
	if choice.isdigit() :
		op = int(choice)
		if op == 1 :
			cpLib(srcLibPath, sysLibPath)
		elif op == 2 :
			print('************ proxy operation **************')
			print('************ 1.get proxy   2.set proxy  3.del proxy **************')
			choice = str(input())
			if choice.isdigit() :
				op = int(choice)
				if op < 1 or op > 3 :
					clearScreen()
					print('######[ERROR]: please make a right choice #####')
				else :
					controlProxy(op, proxy);
			else :	
				clearScreen()
				print('######[ERROR]: please enter a number #####')
		elif op == 3 :
			pass
		elif op == 4 :
			os.popen('start /wait cmd.exe @cmd /k python cdh_logcat.py ' + str(DEBUG))
		elif op == 5 :
			initdata(configPath)
		elif op == 6 :
			executeCmd(adbReboot)
		elif op == 0 :
			clearScreen()
			exit()
		else :
			clearScreen()
			print('######[ERROR]: please enter a number #####')
	action()
########################### function action ######################################


########################### function initdata ##################################
def initdata(path):
	if DEBUG:
		print('######[DEBUG]: init start #####')

	file = open(path, "rb")
	configs = json.load(file)


	global clientIP
	global port
	global sysLibPath
	global srcLibPath
	global proxy

	proxyIP = configs["proxyIP"]
	proxyPort = configs["proxyPort"]
	sysLibPath = configs["sysLibPath"]
	clientIP = configs["clientIP"]
	port = configs["port"]
	project = configs["project"]
	libPath = configs["libPath"]

	proxy = proxyIP + ":" + proxyPort
	srcLibPath = libPath + "\\" + project + "\\Sraf_Browser_SDK\\armeabi-v7a\\"

	if DEBUG:
		print("######[DEBUG]: proxyIP:" + proxyIP  + ' #####')
		print("######[DEBUG]: proxyPort:" + proxyPort + ' #####')
		print("######[DEBUG]: clientIP:" + clientIP + ' #####')
		print("######[DEBUG]: port:" + port + ' #####')
		print("######[DEBUG]: proxy:" + proxy + ' #####')
		print("######[DEBUG]: srcLibPath:" + srcLibPath + ' #####')

		print('######[DEBUG]: init end #####')

########################### function initdata ##################################


########################### function main ##########################################
def main():
	clearScreen()
	print('######[INFO]: START #####')
	#init data from srafconfig.json
	initdata(configPath);

	#connect
	result = executeCmd(adbDisconnect)
	result = executeCmd(adbConnect +  ' ' + clientIP + ':' + port)
	if len(result) == 0:
		print('######[ERROR]: connect failed #####')
		return

	if result[0].find('connected') != -1:
		print('######[INFO]: connet to '+ clientIP + ' success! #####')
		#root
		result = executeCmd(adbRoot)

		if len(result) == 0:
			print('######[INFO]: adb root success! #####')
			#remount
			result = executeCmd(adbRemount)
			if len(result) != 0 and result[0].find('succeeded') != -1:
				print('######[INFO]: adb remount success! #####')
				action()
			else:
				print('######[ERROR]: remount failed #####')
		else:
			print('######[ERROR]: root failed #####')
	else:
		print('######[ERROR]: connect failed #####')
########################### function main ##########################################


if __name__ == '__main__':
	if len(sys.argv) == 2:
		DEBUG = True
	else :
		DEBUG = False
	main()
