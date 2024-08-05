import socket
import time
import logging
from logging.handlers import RotatingFileHandler

# Logger class providing remote syslog capabilities
class Logger:
    LOG_DEBUG = 7
    LOG_INFO = 6
    LOG_WARN = 4
    LOG_ERROR = 3

    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, Server, Port,console_only: bool = False):
        self.console_only: bool = console_only
        self.Server = Server
        self.Port = Port
        if not self.console_only:
            self.log_level = Logger.LOG_INFO
            logging.basicConfig(handlers=[RotatingFileHandler('./IOT_Connector.log', maxBytes=2000000, backupCount=10)], level=self.log_level, format="[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s", datefmt='%Y-%m-%dT%H:%M:%S')
            self.logger = logging.getLogger()
            print("Opening syslog...")

    # ************************************************************************
    # Send debug Log Message
    # ************************************************************************
    def debug(self, message):
        self.__sendLogMsg(Logger.LOG_DEBUG, message)

    # ************************************************************************
    # Send Warning Log Message
    # ************************************************************************
    def warn(self, message):
        self.__sendLogMsg(Logger.LOG_WARN, message)

    # ************************************************************************
    # Send Error Log Message
    # ************************************************************************
    def err(self, message):
        self.__sendLogMsg(Logger.LOG_ERROR, message)

    # ************************************************************************
    # Send Info Log Message
    # ************************************************************************
    def info(self, message):
        self.__sendLogMsg(Logger.LOG_INFO, message)

    # ************************************************************************
    # Send Log Message
    # ************************************************************************
    def __sendLogMsg(self, level, message):

        if level == Logger.LOG_DEBUG:
            print("\x1b[94mDEBUG   : ", end='')
            logging_level = logging.getLevelName("DEBUG")
        if level == Logger.LOG_INFO:
            print("\x1b[96mINFO    : ", end='')
            logging_level = logging.getLevelName("INFO")
        if level == Logger.LOG_WARN:
            print("\x1b[93mWARNING : ", end='')
            logging_level = logging.getLevelName("WARN")
        if level == Logger.LOG_ERROR:
            print("\x1b[91mERROR   : ", end='')
            logging_level = logging.getLevelName("ERROR")

        local_time = time.strftime("%Y-%m-%d %H:%M:%S %Z%z", time.localtime(time.time()))

        print(f"{local_time}: {message}\x1b[0m")
        server_msg = "<" + str(8 + level) + ">" + socket.gethostname() + " IoT Connector: " + message
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(bytes(server_msg, "utf-8"), (self.Server, self.Port))
        except:
            pass

        if not self.console_only:
            self.logger.log(logging_level, message)
