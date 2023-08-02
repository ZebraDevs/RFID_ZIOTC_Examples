import json
import http.client

class RestAPI:

	def __init__(self):
		self.conn = http.client.HTTPConnection("127.0.0.1")
		self.invState = False
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
			return 0, "Non-returned value".encode(encoding="utf-8")

	# ************************************************************************
	# Start Inventory Scan
	# ************************************************************************
	def startInventory(self):
		retry = 0;
		while retry < self.retry_count:
			headers = {}
			status, data = self.__makeRequest("PUT", "/cloud/start", "", headers)
			if status == 200:
				self.invState = True
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
				self.invState = False
				return
			retry = retry + 1

	# ************************************************************************
	# Set configuration
	# ************************************************************************
	def setConfig(self, payload):
		retry = 0;
		while retry < self.retry_count:
			headers = {}
			status, data = self.__makeRequest("PUT", "/cloud/config", payload, headers)
			if status == 200:
				return
			retry = retry + 1

	# ************************************************************************
	# Set Operation Mode
	# ************************************************************************
	def setMode(self, payload):
		retry = 0;
		while retry < self.retry_count:
			headers = {}
			status, data = self.__makeRequest("PUT", "/cloud/mode", payload, headers)
			if status == 200:
				return
			retry = retry + 1

	# ************************************************************************
	# Get the reader serial number
	# ************************************************************************
	def getReaderSerial(self):
		retry = 0;
		while retry < self.retry_count:
			headers = {}
			status, data = self.__makeRequest("GET", "/cloud/version", "", headers)
			if status == 200:
				response = json.loads(data.decode("utf-8"))
				return response["serialNumber"]
			retry = retry + 1
		return ""

	# ************************************************************************
	# Retrieve current inventory state
	# ************************************************************************
	def getInventoryState(self):
		return self.invState

restAPI = RestAPI()

# Initial GPO State Configuration
config = {"GPIO-LED": {}}
config["GPIO-LED"]["GPODefaults"] = {}
config["GPIO-LED"]["GPODefaults"]["1"] = "LOW"
config["GPIO-LED"]["GPODefaults"]["2"] = "LOW"
config["GPIO-LED"]["GPODefaults"]["3"] = "LOW"
config["GPIO-LED"]["GPODefaults"]["4"] = "LOW"
restAPI.setConfig(json.dumps(config))

# Set Operation Mode
config = {}
config["type"] = "CUSTOM"
config["tagMetaData"] = ["ANTENNA", "RSSI", "SEEN_COUNT"]
config["environment"] = "AUTO_DETECT"
config["reportFilter"] = {"duration": 0, "type": "RADIO_WIDE"}
restAPI.setMode(json.dumps(config))


# Start the Inventory Scan
restAPI.startInventory()
