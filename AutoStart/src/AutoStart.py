import json
import http.client
import signal
import time
import ssl

class RestAPI:

	def __init__(self):
		self.ssl_context = ssl._create_unverified_context()
		self.conn = http.client.HTTPSConnection("127.0.0.1", context=self.ssl_context)
		self.retry_count = 3

	# ************************************************************************
	# Perform Request
	# ************************************************************************
	def __makeRequest(self, verb, url, payload, headers):
		try:
			self.conn.connect()
			self.conn.request(verb, url, payload, headers)
			res = self.conn.getresponse()
			data = res.read()
			status = res.status
			self.conn.close()
			print("Status " + str(status) + "->" + data)
			return status, data
		except:
			return 500, "Non-returned value".encode(encoding="utf-8")

	# ************************************************************************
	# Start Inventory Scan
	# ************************************************************************
	def startInventory(self):
		retry = 0;
		while retry < self.retry_count:
			headers = {}
			status, data = self.__makeRequest("PUT", "/cloud/start", "", headers)
			if status == 200:
				return
			retry = retry + 1

	# ************************************************************************
	# Stop Invertory Scan
	# ************************************************************************
	def stopIventory(self):
		retry = 0;
		while retry < self.retry_count:
			headers = {}
			status, data = self.__makeRequest("PUT", "/cloud/stop", "", headers)
			if status == 200:
				return
			retry = retry + 1

# ************************************************************************
# Stop Signal Handler
# ************************************************************************
def sigHandler(signum,frame):
    global Stop
    Stop = True

Stop = False
restAPI = RestAPI()
signal.signal(signal.SIGINT,sigHandler)

# Start the Inventory Scan
restAPI.startInventory()

# Loop Until stopped
while not Stop:
    time.sleep(0.2)


restAPI.stopIventory()