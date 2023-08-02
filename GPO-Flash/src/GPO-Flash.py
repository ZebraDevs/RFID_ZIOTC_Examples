import ziotc
import threading
import time
import json

Stop = False
ziotcObject = ziotc.ZIOTC()

# Called when new message recieved from IoT connector
def new_msg_callback(msg_type, msg_in):
	global ziotcObject
	ziotcObject.send_next_msg(zitoc.ZIOTC_MSG_TYPE_DATA, msg_in)

# Background thread that flashes the GPO port 1
def Flash_Thread():
	global Stop
	global ziotcObject
	GPIOState = True
	Port = 1
	FlashTimer = time.time() + 0.5
	while not Stop:
		time.sleep(0.1)
		if FlashTimer < time.time():
			GPIOState = not GPIOState
			msg = {"type":"GPO","pin":Port,"state": "HIGH" if GPIOState else "LOW" }
			ziotcObject.send_next_msg(ziotc.ZIOTC_MSG_TYPE_GPO, bytearray(json.dumps(msg).encode('utf-8')))
			FlashTimer = time.time() + 0.5

# Start Worker Thread
flashThread = threading.Thread(target=Flash_Thread)
flashThread.start()

# Loop processing IoT messages
ziotcObject.reg_new_msg_callback(new_msg_callback)
ziotcObject.loop.run_forever()

# Clean up after stopping
Stop = True
flashThread.join()
