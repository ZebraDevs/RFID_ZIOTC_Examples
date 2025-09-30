# ATR-Viewer

This debian package can be loaded onto the ATR reader to demonstrate the ATR's beam stearing technology. 

## Usage

To use IoT connector must be connected and configured to have a secure WebSocket output for the Tag Data.

After the application has been installed and started it can be browsed to at the ATR's address.

http://x.x.x.x:8181

A Tag with the EPC : BBBB00000000000000000001 is used to tracking.

## Building

The index.html file contains the webpage being displayed, This also set the mode / starts and stops the reader. This can be modified for your own purposes for demonstartions

After modifing the index.html file, This debian package can be rebuilt and installed on the reader.

The EPC Tag along with the operation mode is sent from the HTML file and can also be edited.

