# FX-Package

Fx-Package is a cross-platform application to build debian packages for IoT connector. 

## Usage
`FX-Package -name=Sample -maintainer=G.Crean -version=1.0.0`

* FX-Package.exe - Windows ( 64 Bit)
* FX-Package.elf - Linux ( 64 Bit )
* FX-Package-amd64 - MacOs ( amd64 )
* FX-Package-arm64 - MacOs ( arm64 )


## Folder Structure

- Application
  - src ( Contains the Python source files)
  - pkg ( Contains any other files, ie. config files)
  - out ( Destination folder for the .deb file)


  