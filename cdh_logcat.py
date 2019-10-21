'''
dis: adb command
date: 2019-10-09
author: mlgc4869
'''

import os
import sys

################################# global variable ##################################
adbLogcat = 'adb logcat '

logPath = r'E:\android\log\%date:~0,4%-%date:~5,2%-%date:~8,2%-%time:~0,2%-%time:~3,2%-%time:~6,2%.log'

DEBUG = False
################################# global variable ##################################


########################### function clearScreen ####################################
def clearScreen():
	os.system('cls')
########################### function clearScreen ####################################


########################### function logcat ####################################
def logcat(opt, path):
	print('logcat enter: opt:' + str(opt) + "  path:" + path)
	if DEBUG == 'True':
		print('######[DEBUG]:  path: ' + path + ' #####')
	if opt == 1 :
		os.system(adbLogcat + ' -c ')
	elif opt == 2:
		os.system(adbLogcat)
	elif opt == 3 :
		if len(path) == 0 :
			print('######[ERROR]: path is empty #####')
		os.system(adbLogcat + ' > ' + path)
	else:
		pass
	print('######[INFO]:  logcat finish! #####')
	# os.system('exit')
########################### function logcat ####################################


########################### function main ####################################
def main():
	print(sys.argv)
	if len(sys.argv) == 2:
		DEBUG = sys.argv[1]
	print('************ logcat operation **************')
	print('************ 1.clear log   2.logcat  3.logcat to file **************')
	choice = str(input())
	if choice.isdigit() :
		op = int(choice)
		logcat(op, logPath)
	else :
		print('######[ERROR]: choose error #####')
########################### function main ####################################



if __name__ == '__main__':
	main()