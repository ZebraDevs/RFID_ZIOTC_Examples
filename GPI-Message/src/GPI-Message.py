import ziotc
import json

ziotcObject = ziotc.ZIOTC()

# Called when new message recieved from IoT connector
def new_msg_callback(msg_type, msg_in):
	global ziotcObject
	if msg_type == ziotc.ZIOTC_MSG_TYPE_GPI:
		msg = json.loads(msg_in)
		data = {}
		data["pin"] = msg["pin"]
		data["state"] = msg["state"]
		ziotcObject.send_next_msg(ziotc.ZIOTC_MSG_TYPE_DATA, bytearray(json.dumps(data).encode('utf-8')))

# Loop processing IoT messages
ziotcObject.reg_new_msg_callback(new_msg_callback)
ziotcObject.enableGPIEvents()
ziotcObject.loop.run_forever()

