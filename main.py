#coding:utf-8

import time
import traceback
import sys
import os
import _thread
from optparse import OptionParser
import logging

loggerList = []
loggerSub = logging.getLogger("Sub")
logger = logging.getLogger(__name__)
loggerList.append(loggerSub)
loggerList.append(logger)

formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(thread)d][%(filename)s:%(lineno)d]%(message)s")
fileHandler = logging.FileHandler(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".log",encoding="utf-8")
fileHandler.setFormatter(formatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)

from shadowsocksR import SSRParse,SSR
from speedTest import SpeedTest,setInfo
from exportResult import exportAsPng,exportAsJson
import importResult
#from socks2http import ThreadingTCPServer,SocksProxy
#from socks2http import setUpstreamPort

VERSION = "0.2b"
LOCAL_ADDRESS = "127.0.0.1"
LOCAL_PORT = 1087

def setOpts(parser):
	parser.add_option(
		"-c","--config",
		action="store",
		dest="guiConfig",
		default="",
		help="Load config generated by shadowsocksr-csharp."
		)
	parser.add_option(
		"-u","--url",
		action="store",
		dest="url",
		default="",
		help="Load ssr config from subscription url."
		)
	parser.add_option(
		"-m","--method",
		action="store",
		dest="test_method",
		default="cachefly",
		help="Select test method in speedtestnet,cachefly and fast"
		)
	parser.add_option(
		"-f","--filter",
		action="store",
		dest="filter",
		default = "",
		help="Filter nodes by group and remarks using keyword."
		)
	parser.add_option(
		"--fr","--fremark",
		action="store",
		dest="remarks",
		default="",
		help="Filter nodes by remarks using keyword."
		)
	parser.add_option(
		"--fg","--fgroup",
		action="store",
		dest="group",
		default="",
		help="Filter nodes by group name using keyword."
		)
	parser.add_option(
		"-y","--yes",
		action="store_true",
		dest="confirmation",
		default=False,
		help="Skip node list confirmation before test."
		)
	parser.add_option(
		"-e","--export",
		action="store",
		dest="export_file_type",
		default="",
		help="Export test result to json or png file,now supported 'png' or 'json'"
		)
	parser.add_option(
		"-i","--import",
		action="store",
		dest="import_file",
		default="",
		help="Import test result from json file and export it."
		)
	parser.add_option(
		"--debug",
		action="store_true",
		dest="debug",
		default=False,
		help="Run program in debug mode."
		)

def export(Result,exType):
	if (exType.lower() == "png"):
		exportAsPng(Result)
	elif ((exType.lower() == "json") or (exType == "")):
		exportAsJson(Result)
	else:
		logger.error("Unsupported export type %s" % exType)
		exportAsJson(Result)

if (__name__ == "__main__"):
	setInfo(LOCAL_ADDRESS,LOCAL_PORT)
	#setUpstreamPort(LOCAL_PORT)

	DEBUG = False
	CONFIG_LOAD_MODE = 0 #0 for import result,1 for guiconfig,2 for subscription url
	CONFIG_FILENAME = ""
	CONFIG_URL = ""
	IMPORT_FILENAME = ""
	FILTER_KEYWORD = ""
	FILTER_GROUP_KRYWORD = ""
	FILTER_REMARK_KEYWORD = ""
	TEST_METHOD = ""
	SKIP_COMFIRMATION = False
	EXPORT_TYPE = ""

	
	parser = OptionParser(usage="Usage: %prog [options] arg1 arg2...",version="SSR Speed Tool " + VERSION)
	setOpts(parser)
	(options,args) = parser.parse_args()

	#print(options.test_method)
	if (options.test_method == "speedtestnet"):
		TEST_METHOD = "SPEED_TEST_NET"
	elif(options.test_method == "fast"):
		TEST_METHOD = "FAST"
	elif(options.test_method == "cachefly"):
		TEST_METHOD = "CACHE_FLY"
	else:
		TEST_METHOD = "CACHE_FLY"

	if (options.debug):
		DEBUG = options.debug
		for item in loggerList:
			item.setLevel(logging.DEBUG)
			item.addHandler(fileHandler)
			item.addHandler(consoleHandler)
	else:
		for item in loggerList:
			item.setLevel(logging.INFO)
			item.addHandler(fileHandler)
			item.addHandler(consoleHandler)


	if (options.confirmation):
		SKIP_COMFIRMATION = options.confirmation

	if (len(sys.argv) == 1):
		parser.print_help()
		exit(0)

	if (options.import_file):
		CONFIG_LOAD_MODE = 0
	elif (options.guiConfig):
		CONFIG_LOAD_MODE = 1
		CONFIG_FILENAME = options.guiConfig
	elif(options.url):
		CONFIG_LOAD_MODE = 2
		CONFIG_URL = options.url
	else:
		logger.error("No config input,exiting...")
		sys.exit(1)


	if (options.filter):
		FILTER_KEYWORD = options.filter
	if (options.group):
		FILTER_GROUP_KRYWORD = options.group
	if (options.remarks):
		FILTER_REMARK_KEYWORD = options.remarks

	if (options.export_file_type):
		EXPORT_TYPE = options.export_file_type.lower()

	if (options.import_file and CONFIG_LOAD_MODE == 0):
		IMPORT_FILENAME = options.import_file
		export(importResult.importResult(IMPORT_FILENAME),EXPORT_TYPE)
		sys.exit(0)

	#socks2httpServer = ThreadingTCPServer((LOCAL_ADDRESS,FAST_PORT),SocksProxy)
	#_thread.start_new_thread(socks2httpServer.serve_forever,())
	#print("socks2http server started.")
	ssrp = SSRParse()
	if (CONFIG_LOAD_MODE == 1):
		ssrp.readGuiConfig(CONFIG_FILENAME)
	else:
		ssrp.readSubscriptionConfig(CONFIG_URL)
	ssrp.filterNode(FILTER_KEYWORD,FILTER_GROUP_KRYWORD,FILTER_REMARK_KEYWORD)
	ssrp.printNode()
	if (not SKIP_COMFIRMATION):
		ans = input("Before the test please confirm the nodes,Ctrl-C to exit. (Y/N)")
		if (ans == "Y"):
			pass
		else:
			sys.exit(0)

	'''
		{
			"group":"",
			"remarks":"",
			"loss":0,
			"ping":0.01,
			"gping":0.01,
			"dspeed":10214441 #Bytes
		}
	'''
	Result = []
	retryList = []
	retryConfig = []
	retryMode = False
#	exit(0)

	ssr = SSR()
	config = ssrp.getNextConfig()
	while(True):
		_item = {}
		_item["group"] = config["group"]
		_item["remarks"] = config["remarks"]
		ssr.startSsr(config)
		logger.info("Starting test for %s - %s" % (_item["group"],_item["remarks"]))
		time.sleep(1)
		try:
			st = SpeedTest()
			latencyTest = st.tcpPing(config["server"],config["server_port"])
			time.sleep(1)
			#_thread.start_new_thread(socks2httpServer.serve_forever,())
			#logger.debug("socks2http server started.")
			_item["dspeed"] = st.startTest(TEST_METHOD)
			time.sleep(0.2)
			ssr.stopSsr()
			time.sleep(0.2)
			ssr.startSsr(config)
		#	.print (latencyTest)
			_item["loss"] = 1 - latencyTest[1]
			_item["ping"] = latencyTest[0]
		#	_item["gping"] = st.googlePing()
			_item["gping"] = 0
			if ((int(_item["dspeed"]) == 0) and (retryMode == False)):
				retryList.append(_item)
				retryConfig.append(config)
			else:
				Result.append(_item)
			logger.info("%s - %s - Loss:%s%% - TCP_Ping:%d - Google_Ping:%d - Speed:%.2f" % (_item["group"],_item["remarks"],_item["loss"] * 100,int(_item["ping"] * 1000),int(_item["gping"] * 1000),_item["dspeed"] / 1024 / 1024) + "MB")
			#socks2httpServer.shutdown()
			#logger.debug("Socks2HTTP Server already shutdown.")
		except Exception:
			ssr.stopSsr()
			#socks2httpServer.shutdown()
			#logger.debug("Socks2HTTP Server already shutdown.")
			#traceback.print_exc()
			logger.exception("")
			sys.exit(1)
		ssr.stopSsr()
		if (retryMode):
			if (retryConfig != []):
				config = retryConfig.pop(0)
			else:
				config = None
		else:
			config = ssrp.getNextConfig()

		if (config == None):
			if ((retryMode == True) or (retryList == [])):
				break
			ans = str(input("%d node(s) got 0kb/s,do you want to re-test these node? (Y/N)" % len(retryList))).lower()
			if (ans == "y"):
			#	logger.debug(retryConfig)
				retryMode = True
				config = retryConfig.pop(0)
			#	logger.debug(config)
				continue
			else:
				for r in retryList:
					Result.append(r)
				break

	export(Result,EXPORT_TYPE)
	ssr.stopSsr()
	#if (socks2httpServer):
		#socks2httpServer.shutdown()
		#logger.debug("Socks2HTTP Server already shutdown.")
	sys.exit(0)
#	ssr.stopSsr()

