import pyziotc
import json
import os
import traceback
import time
import signal
from Logger import Logger
from RestAPI import RestAPI

# Global Variables
UDP_PORT = 9000
DEBUG_SERVER = "192.168.13.140"
DEBUG_PORT = 40514
LOG_ONLY_TO_CONSOLE = False
REST_API_RETRY_COUNT = 3

Stop = False
ziotcObject = pyziotc.Ziotc()
logger = Logger(DEBUG_SERVER, DEBUG_PORT, LOG_ONLY_TO_CONSOLE)
restAPI = RestAPI(logger, REST_API_RETRY_COUNT,ziotcObject)

# ************************************************************************
# Stop Signal Handler
# ************************************************************************
def sigHandler(signum,frame):
	global Stop
	Stop = True

# ************************************************************************
# New Event Received
# ************************************************************************
def new_msg_callback(msg_type, msg_in):
    if msg_type == pyziotc.MSG_IN_JSON:
        process_tag(msg_in)

# ************************************************************************
# Process Tag Event
# ************************************************************************
def process_tag(msg_in):
	msg_in_json = json.loads(msg_in)
	tag_id_hex = msg_in_json["data"]["idHex"]
	ziotcObject.send_next_msg(pyziotc.MSG_OUT_DATA, bytearray((tag_id_hex + "\n").encode('utf-8')))

# ************************************************************************
# Entry Point
# ************************************************************************
signal.signal(signal.SIGINT,sigHandler)

logger.debug("System Started:  " + str(os.getpid()))
logger.debug("Reader Version: " + restAPI.getReaderVersion())
logger.debug("Reader Serial Number: " + restAPI.getReaderSerial())
logger.debug("Script Version: " + str(os.getenv("VERSION")))

# Register callbacks
ziotcObject.reg_new_msg_callback(new_msg_callback)

# Start Inventory Scan
restAPI.startInventory()

# Loop Forever ( Ish )
while not Stop:
	time.sleep(0.2)
		
# Clean up
restAPI.stopInventory()
logger.info("Stopped")
