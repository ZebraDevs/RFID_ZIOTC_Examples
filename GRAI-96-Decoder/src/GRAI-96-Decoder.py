# GRAI-96 Decoder By G.Crean
# (c)2023 Zebra Technologies
import pyziotc
import json
import signal
import time

# Global Variables
Stop = False
ziotcObject = pyziotc.Ziotc()

# ************************************************************************
# Stop Signal Handler
# ************************************************************************
def sigHandler(signum,frame):
    global Stop
    Stop = True
    
# ************************************************************************
# Called when new message recieved from IoT connector
# ************************************************************************
def new_msg_callback(msg_type, msg_in):
    if msg_type == pyziotc.MSG_IN_JSON:
        msg_in_json = json.loads(msg_in.decode('utf-8'))
        tag_id_hex = msg_in_json["data"]["idHex"] 
        if not tag_id_hex.startswith("33"):
        	return
        bin = f'{int(tag_id_hex,16):0>96b}'

        Header = str(int(bin[0:8],2))
        Filter = str(int(bin[8:11],2))
        Partition = int(bin[11:14],2)
        if Partition == 0:
            CompanyBits = 40
            AssetBits = 4
        elif Partition == 1:
            CompanyBits = 37
            AssetBits = 7
        elif Partition == 2:
            CompanyBits = 34
            AssetBits = 10
        elif Partition == 3:
            CompanyBits = 30
            AssetBits = 14
        elif Partition == 4:
            CompanyBits = 27
            AssetBits = 17
        elif Partition == 5:
            CompanyBits = 24
            AssetBits = 20
        elif Partition == 6:
            CompanyBits = 20
            AssetBits = 24
        else:
            return             

        Company = str(int(bin[14:14+CompanyBits],2))
        AssetType =  str(int(bin[14+CompanyBits:14+CompanyBits+AssetBits],2))
        Serial = str(int(bin[14+CompanyBits+AssetBits:],2))

        #Construct JSON payload
        tag = {}
        tag["Antenna"] = msg_in_json["data"]["antenna"]
        tag["RSSI"] = msg_in_json["data"]["peakRssi"]
        tag["Filter"] = Filter
        tag["Partition"] = Partition
        tag['SerialNumber'] = Serial
        tag["Company"] = Company
        tag["AssetType"] = AssetType
        tag["Urn"] = "urn:epc:tag:grai-96:" +Filter + "." + Company + "." + AssetType + "." + Serial
        tag["Epc"] = tag_id_hex
        ziotcObject.send_next_msg(pyziotc.MSG_OUT_DATA, bytearray(json.dumps(tag).encode('utf-8')))

# ************************************************************************
# Entry Point
# ************************************************************************
signal.signal(signal.SIGINT,sigHandler)

# Register callbacks
ziotcObject.reg_new_msg_callback(new_msg_callback)

# Loop Until stopped
while not Stop:
    time.sleep(0.2)
