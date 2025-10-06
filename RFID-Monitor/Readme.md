# RFID-Monitor

This debian package can be loaded onto the reader to demonstrate antenna reads 

## Usage

To use IoT connector must be connected and configured to have a secure WebSocket output for the Tag Data.

After the application has been installed and started it can be browsed to at the readers address.

https://x.x.x.x:8181

## Building

The index.html file contains the webpage being displayed.

the keys folder is intially empty, and when is available will create a secure web socket by createing the CA and device certs on startup.
