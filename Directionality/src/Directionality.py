import pyziotc
import json
import os
import traceback
import datetime
import time
import uuid
import signal
from queue import Queue
from Logger import Logger
from RestAPI import RestAPI

# Config.ini File settings
from INIFile import INIFile
if os.environ.get('INI_LOCATION') is not None:
    Ini = INIFile(os.getenv('INI_LOCATION'))
else:
    Ini = INIFile("config.ini")

# Global Config Parameters
DEBUG_SERVER = Ini.getStr("General", "DebugServer", "")
DEBUG_PORT = Ini.getInt("General", "DebugPort", 40514)
LOG_ONLY_TO_CONSOLE = Ini.getBool("General", "Log_Only_To_Console", False)
REST_API_RETRY_COUNT = Ini.getInt("General", "Retry", 3) 

# Global Variables
Stop = False
TagEntries = {}
ziotcObject = pyziotc.Ziotc()
logger = Logger(DEBUG_SERVER, DEBUG_PORT, LOG_ONLY_TO_CONSOLE)
restAPI = RestAPI(logger, REST_API_RETRY_COUNT,ziotcObject)

# GPI Events State Machine
STATE_WAITING = 0
STATE_WAIT_GPI1_ON = 1
STATE_WAIT_GPI2_ON = 2
STATE_WAIT_OFF = 3
State = STATE_WAITING
GPI_1 = False
GPI_2 = False
Direction=""

# ************************************************************************
# Stop Signal Handler
# ************************************************************************
def sigHandler(signum,frame):
	global Stop
	Stop = True

# ************************************************************************
# Passthrough callback
# ************************************************************************
def passthru_callback(msg_in):
    Logger.sendLogMsg(Logger.LOG_WARN, msg_in)
    return b"unrecognized command"

# ************************************************************************
# New Event Received
# ************************************************************************
def new_msg_callback(msg_type, msg_in):
    if msg_type == pyziotc.MSG_IN_GPI:
        process_gpi(msg_in)

    if msg_type == pyziotc.MSG_IN_JSON:
        process_tag(msg_in)

# ************************************************************************
# Process GPI Events
# ************************************************************************
def process_gpi(msg_in):
	global State
	global Direction
	global TagEntries
	global GPI_1
	global GPI_2

	# Get Message Contents
	msg = json.loads(msg_in)
	pin = msg["pin"]
	pin_state = False if msg["state"] == "HIGH" else True
	logger.debug("Pin : " + str(pin) + " State : " + str(pin_state))

	# Store the pin values
	if pin == 1:
		GPI_1 = pin_state

	if pin == 2:
		GPI_2 = pin_state	

	logger.debug("State : " + str(State))
	# If GPI 1 is triggered first, Then we are moving out
	if State == STATE_WAITING and GPI_1 == True:
		State = STATE_WAIT_GPI2_ON
		restAPI.startInventory()
		Direction = "Out"

	# If GPI 2 is triggered first, Then we are moving in
	if State == STATE_WAITING and GPI_2 == True:
		State = STATE_WAIT_GPI1_ON
		restAPI.startInventory()
		Direction = "In"

	# Waiting for GPI 1 to go on.
	if State == STATE_WAIT_GPI1_ON and GPI_1 == True:
		State = STATE_WAIT_OFF

	# Waiting for GPI 2 to go on	
	if State == STATE_WAIT_GPI2_ON and GPI_2 == True:
		State = STATE_WAIT_OFF

	# Wait for GPI's to be off
	if State == STATE_WAIT_OFF and GPI_1 == False and GPI_2 == False:
		restAPI.stopInventory()
		if State == STATE_WAIT_OFF:
			publishData()
		TagEntries.clear()
		State = STATE_WAITING

	logger.debug("Next State : " + str(State))

# ************************************************************************
# Publish the Data
# ************************************************************************
def publishData():
	global TagEntries
	global Direction
	global ziotcObject

	for idx in list(TagEntries):
		tag = TagEntries[idx]
		tag["direction"] = Direction
		ziotcObject.send_next_msg(pyziotc.MSG_OUT_DATA, bytearray(json.dumps(tag).encode('utf-8')))

# ************************************************************************
# Process Tag Event
# ************************************************************************
def process_tag(msg_in):
	msg_in_json = json.loads(msg_in)
	tag_id_hex = msg_in_json["data"]["idHex"]

	if not tag_id_hex in TagEntries:
		TagEntries[tag_id_hex] = msg_in_json

# ************************************************************************
# Entry Point
# ************************************************************************
signal.signal(signal.SIGINT,sigHandler)

# Report details
logger.debug("System Started:  " + str(os.getpid()))
logger.debug("Reader Version: " + restAPI.getReaderVersion())
logger.debug("Reader Serial Number: " + restAPI.getReaderSerial())
logger.debug("Script Version: " + str(os.getenv("VERSION")))

# Register callbacks
ziotcObject.reg_new_msg_callback(new_msg_callback)
ziotcObject.reg_pass_through_callback(passthru_callback)
ziotcObject.enableGPIEvents()

# Loop Forever
while not Stop:
	time.sleep(0.2)

# Clean up
restAPI.stopInventory()
logger.info("Stopped")
