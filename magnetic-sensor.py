#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import serial.tools.list_ports
import os
import logging
import argparse
import datetime
from datetime import datetime, timedelta
import telebot

# Configure logging
logging.basicConfig(
   format="%(asctime)s %(levelname)s %(filename)s:%(funcName)s():%(lineno)i: %(message)s",
   datefmt="%Y-%m-%d %H:%M:%S",
   level=logging.DEBUG)
logger = logging.getLogger(__name__)


def print_port() -> None:
   # get list of serial ports
   ports = list(serial.tools.list_ports.comports())
  
   # print ports
   print("Ports found:")
   for port in ports:
       if "VID:PID=0D28:0204" in port[2].upper():
           print(f"    {port}")
   print()


def loop(serial_port: str) -> None:
   # open the serial port
   with serial.Serial(serial_port, 115200, timeout=1) as ser:
       print("Press Ctrl-C to stop")
       print("--------------------")

       reminder_time = datetime.now()
       takenFlag = 0

       try:
           # loop forever
           while True:

               # read a line from the serial port
               line = ser.readline().decode('utf-8').strip()

               # if the read was successful, do something with it
               if line:
                   if line == "0": # this will always occur when a reminder from microbit A is sent - this is to calculate med timeout
                      reminder_time = datetime.now() + timedelta(minutes=5) # currently set to 5 seconds
                      takenFlag = 0
                   
                   if line == "1": # this is when the pill is taken
                      takenFlag = 1 # for meds not taken purposes - flag will change to 1 to show it has been taken
                      msg = "Medication has been taken at " + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "."
                      bot.send_message(691448132, msg)
                   
               if reminder_time.strftime('%d/%m/%Y %H:%M:%S') == datetime.now().strftime('%d/%m/%Y %H:%M:%S') and takenFlag == 0: # beyond timeout and meds hasn't been taken yet
                   ser.write("3".encode()) # sends to microbit for the sound to stop - I hardcoded this, so if this is changed, microbit code also need to change
                   bot.send_message(691448132, "Medication has not been taken 5 minutes after reminder.")
                   
       except KeyboardInterrupt:
           print()
           print("Magnetic sensor script stopped.")


def main() -> None:


   # Parse arguments
   parser = argparse.ArgumentParser()
   parser.add_argument("port", nargs="?")
   args = parser.parse_args()
   args_port = args.port


   if args_port:
       print_port()
       print(f"Using serial port: {args_port}")
   else:
       print(f"Error: must specify the serial port 💤")
       print(f"Example:")
       print()
       print(f"    python {os.path.basename(__file__)} INSERT_YOUR_SERIAL_PORT_HERE")
       print()
       print(f"Not a valid serial port, see below for possible serial ports:")
       print_port()
       exit()


   loop(args_port)


if __name__ == "__main__":
   bot = telebot.TeleBot(token='6045647581:AAELiwZ_KseUmVkfV2xGF81rZXM9iSp3amY')
   main()
