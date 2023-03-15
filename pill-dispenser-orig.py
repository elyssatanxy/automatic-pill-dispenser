from guizero import App, Box, Text, TextBox, PushButton, Window
from guizero import info
import serial
from serial.serialutil import SerialException
from serial.tools import list_ports

# NOTE: connecting and disconnecting functions will be removed in final implementation, just for me to check
# connect to microbit via serial port
def connect():
	try:
		ser.open()
	except SerialException:
		info("Error", "Unplug microbit and try again")
		

# disconnect from microbit
def disconnect():
	ser.close()


# send number for timer
def send_data():
	global timer
	send_this = str(timer) + "\n"
	print("sending value: ", send_this)
	
	try:
		ser.write(send_this.encode())
	except SerialException:
		info("Error", "Could not send.")

# increment timer value
def increment_timer():
	global timer
	timer += 1
	print("updated timer to", timer)
	timer_text.value = timer


# decrement timer value
def decrement_timer():
	global timer
	if (timer-1 > -1):
		timer -= 1
		print("updated timer to", timer)
		timer_text.value = timer
	else: 
		print("timer cannot be negative", timer)

# COMPLETED: stop and reset the timer immediately
def reset_timer():
	global timer
	timer = 0
	send_data()
	timer_text.value = timer
	print("timer reset to 0")

# find port number of microbit
def find_microbit_comport():
	ports = list(list_ports.comports())
	for p in ports:
		if (p.pid == 516) and (p.vid == 3368):
			return str(p.device)
	

# SET UP CONNECTION
ser = serial.Serial()
ser.baudrate = 115200
ser.port = find_microbit_comport()
ser.open()


# START OF GUI
app = App(title="pill dispenser")

# LAYOUT 
Text(app, text="	", height = 3)
menu = Box(app, align="top", width="fill")
content_box = Box(app, align="top", width="fill")

connect_box = Box(content_box, align="right", height="fill")
Text(app, text="	", height = 3)
timer_box = Box(app, layout="grid", align="top")
Text(app, text="	", height = 3)
datasig_box = Box(app, layout="grid", align="top")

#APP TITLE
intro = Text(menu, text="Pill Dispensing", size=40, align="top")

# NOTE: these buttons will be removed to avoid any tampering
disconnect_button = PushButton(connect_box, text = "Disconnect", command=disconnect, align="right")
connect_button = PushButton(connect_box, text = "Connect", command=connect, align="right")

# BUTTONS FOR ADJUSTING TIMER
decrement_button = PushButton(timer_box, text = "-", command=decrement_timer, grid=[0,1])
Text(timer_box, text="	", grid=[1,1])
Text(timer_box, text="	", grid=[3,1])
increment_button = PushButton(timer_box, text = "+", command=increment_timer, grid=[4,1])

reset_button = PushButton(datasig_box, text = "reset", command=reset_timer, grid=[0,1])
Text(datasig_box, text="	", grid=[1,1])
send_button = PushButton(datasig_box, text="Send", command=send_data, grid=[2,1])

timer = 0
timer_text = Text(timer_box, text = timer, size=40, grid=[2,1])

#app.set_full_screen()
app.display()