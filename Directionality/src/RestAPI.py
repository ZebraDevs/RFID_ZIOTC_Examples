import pyziotc
import ssl
import base64
import http.client
import json

# Rest API interface
class RestAPI:
    conn = None
    invState = False

    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, logger, retry_count, ziotc):
        self.logger = logger
        self.retry_count = retry_count
        self.ziotcObject = ziotc
        self.GPOState = [ None, None, None, None, None, None, None, None, None ]
        self.__get_jwt()

    # ************************************************************************
    # Get Auth Token
    # ************************************************************************
    def __get_jwt(self):
        self.ssl_context = ssl._create_unverified_context()
        self.conn = http.client.HTTPSConnection("127.0.0.1", context=self.ssl_context)

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
            return status, data
        except:
            return 0, "Non-returned value".encode(encoding="utf-8")

    # ************************************************************************
    # Start Inventory Scan
    # ************************************************************************
    def startInventory(self):
        retry = 0
        payload = "{ \"doNotPersistState\": true }"
        while retry < self.retry_count:
            headers = { }
            status, data = self.__makeRequest("PUT", "/cloud/start", payload, headers)
            if status == 200:
                self.logger.info("Inventory Started")
                self.invState = True
                return
            self.__get_jwt()
            retry = retry + 1
        self.logger.err("Inventory Start Failed :" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Stop Invertory Scan
    # ************************************************************************
    def stopInventory(self):
        retry = 0
        while retry < self.retry_count:
            headers = {}
            status, data = self.__makeRequest("PUT", "/cloud/stop", "", headers)
            if status == 200:
                self.logger.info("Inventory Stopped")
                self.invState = False
                return
            self.__get_jwt()
            retry = retry + 1
        self.logger.err("Inventory Stop Failed :" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Set General Purpose output State
    # ************************************************************************
    def setFastGPO(self, port, state):
        if self.GPOState[port] == state:
            return 

        var = {"type":"GPO","pin":port,"state": "HIGH" if state else "LOW" }
        self.ziotcObject.send_next_msg(pyziotc.MSG_OUT_GPO, bytearray(json.dumps(var).encode('utf-8')))
        self.GPOState[port] = state
        self.logger.info("Set GPO " + str(port) + " -> " + var["state"])

    # ************************************************************************
    # Set General Purpose output State using local rest API
    # ************************************************************************
    def setGPO(self, port, state):
        if self.GPOState[port] == state:
            return

        payload = json.dumps({'port': port, 'state': state})
        retry = 0;
        while retry < self.retry_count:
            headers = {'Content-Type': 'application/json'}
            status, data = self.__makeRequest("PUT", "/cloud/gpo", payload, headers)
            if status == 200:
                self.GPOState[port] = state  
                return
            self.__get_jwt()
            retry = retry + 1
        self.logger.err("Set GPO State failed :" + str(status) + " -> " + data.decode("utf-8"))


    # ************************************************************************
    # Set configuration
    # ************************************************************************
    def setConfig(self, payload):
        retry = 0
        while retry < self.retry_count:
            headers = {'Content-Type': 'application/json'}
            status, data = self.__makeRequest("PUT", "/cloud/config", payload, headers)
            if status == 200:
                return
            self.__get_jwt()
            retry = retry + 1
        self.logger.err("failed to set configuration :" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Set Operation Mode
    # ************************************************************************
    def setMode(self, payload):
        retry = 0
        while retry < self.retry_count:
            headers = {'Content-Type': 'application/json'}
            status, data = self.__makeRequest("PUT", "/cloud/mode", payload, headers)
            if status == 200:
                return
            self.__get_jwt()
            retry = retry + 1
        self.logger.err("failed to operation mode :" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Get the reader version
    # ************************************************************************
    def getReaderVersion(self):
        retry = 0
        while retry < self.retry_count:
            headers = {'Content-Type': 'application/json'}
            status, data = self.__makeRequest("GET", "/cloud/version", "", headers)
            if status != 200:
                self.logger.err("Unable to retrieve reader version :" + str(status) + " -> " + data.decode("utf-8"))
            else:
                response = json.loads(data.decode("utf-8"))
                return response["readerApplication"]
            retry = retry + 1
        self.logger.err("failed to get version number :" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Get the reader serial number
    # ************************************************************************
    def getReaderSerial(self):
        retry = 0
        while retry < self.retry_count:
            headers = {'Content-Type': 'application/json'}
            status, data = self.__makeRequest("GET", "/cloud/version", "", headers)
            if status != 200:
                self.logger.err("Unable to retrieve reader serial :" + str(status) + " -> " + data.decode("utf-8"))
            else:
                response = json.loads(data.decode("utf-8"))
                return response["serialNumber"]
            retry = retry + 1
        self.logger.err("failed to get serial number:" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Set Data Analytics Mode
    # ************************************************************************
    def setPassththrough(self):
        retry = 0
        payload = json.dumps({"component": "RC", "payload": "data_analytics STRING"})

        while retry < self.retry_count:
            headers = {'Content-Type': 'application/json'}
            status, data = self.__makeRequest("PUT", "/cloud/pass-through", payload, headers)
            if status == 200:
                return
            self.__get_jwt()
            retry = retry + 1
        self.logger.err("failed to set pass-through mode :" + str(status) + " -> " + data.decode("utf-8"))

    # ************************************************************************
    # Retrieve current inventory state
    # ************************************************************************
    def getInventoryState(self):
        return self.invState
