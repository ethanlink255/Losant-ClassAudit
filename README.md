# Losant Class Audit

Application for the management of out of class time for schools. 


**WARNING**: This Application is still in development, and should not be used in production

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them

The application is currently broken down into client and server side applications, with install requirements, and shell scripts in each.
#### Hardware

* [Raspberry Pi 3 B+](https://www.raspberrypi.org)
* [Raspberry Pi 7 in. Display](https://www.raspberrypi.org)
* Linux Server

#### Server Side Installation

##### First, execute setup.sh (as root)
```
chmod +x ./Server/setup.sh
sudo ./Server/.setup.sh
```
##### Second, install python3 requirements
```
pip3 install -r ./Server/requirements.txt
```

### Installing

#### Server Side
**Warning**: Project unfinshed, currently server side, the application is ran from Server/REST API/rest.py, but in prodcution should be ran from a WSGI server

#### Client Side
**Warning**: Project unfinshed, currently client side, the application is ran from Client/client.py

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Losant](http://www.losant.com) - Dashboard system used to display data

## Contributing

I welcome contributers to this project!

## Authors

* **Ethan Link** - [Ethan](https://github.com/ethanlink255)

## License

All rights reserved
