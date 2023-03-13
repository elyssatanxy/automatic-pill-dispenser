#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import serial
import serial.tools.list_ports
import os
import sys
import logging
import argparse
import random
import pprint
import time
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


        try:
           # loop forever
            while True:


                # read a line from the serial port
                line = ser.readline().decode('utf-8').strip()

                reminder_time = datetime.now() + timedelta(minutes=5)
                
                while True:
                    # if the read was successful, do something with it
                    if line:
                        print(f"{line}")
                    
                        # this section writes to file
                        f = open("log.txt", "a")
                        f.write(line + " at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
                        f.close()
                        
                        break

                    if reminder_time == datetime.now():
                        bot.send_message(691448132, "Medication has not been taken 5 minutes after reminder.")

                   
        except KeyboardInterrupt:
            print()
            print("kthxbye")


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
       print(f"Huh, simi serial port? See below for possible serial ports:")
       print_port()
       exit()


   loop(args_port)




if __name__ == "__main__":
   bot = telebot.TeleBot(token='6045647581:AAELiwZ_KseUmVkfV2xGF81rZXM9iSp3amY')
   main()
