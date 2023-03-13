from guizero import App, Box, info, Text, TextBox, PushButton
import serial
from serial.serialutil import SerialException
from serial.tools import list_ports

# check data 
def check_data():
    global hour_input, min_input, hours, minutes, og_hrs, og_mins
    
    invalid_input = False
    
    if(len(hour_input.value) == 0):     # checks if textbox is empty
        error_displayhr.hide()
    elif (int(hour_input.value) > 12):  # check if meets constraint
        invalid_input = True            # fails, sets invalid flag = true
        error_displayhr.show()
    else:                               # fufils requirement 
        hours = int(hour_input.value)
        og_hrs = int(hour_input.value)
        error_displayhr.hide()
        
    if(len(min_input.value) == 0):
        error_displaymin.hide()
    elif (int(min_input.value) > 59):
        invalid_input = True
        error_displaymin.show()
    else:
        minutes = int(min_input.value)
        og_mins = int(min_input.value)
        error_displaymin.hide()
        
    if(not invalid_input):              # if flag is false, then send
        send_data()

# send number for timer
def send_data():
    global notification, hours, minutes
    
    seconds = (hours * 60 * 60) + (minutes * 60)
    send_this = str(seconds) + "\n"    
    
    try:
        print("sending value: " + str(hours) + " hr " + str(minutes) + " min = " + str(seconds) + "s" )
        ser.write(send_this.encode())
        if(seconds > 0):
            notification.value = "Next reminder in " + str(hours) + " hr " + str(minutes) + "min"
            notification.show()
        else:
            notification.value = "Timer reset to 0"
            notification.show()
            
    except SerialException:
        info("Error", "Could not send.")
    
# stop and reset the timer immediately
# TODO: prevent microbit dispensing if time sent  == 0
def reset_timer():
    global hours, minutes
    
    error_displayhr.hide()
    error_displaymin.hide()
    min_input.clear()
    hour_input.clear()
    
    hours = 0
    minutes = 0
    
    send_data()
    print("timer reset to 0")

# countdown timer
def counter():
    global hours, minutes, og_hrs, og_mins
    if((minutes-1) == -1):
        hours -= 1
        minutes = 59
    elif((hours-1) == -1):
        hours = og_hrs
        minutes = og_mins
    else:
        minutes -= 1
    notification.value = "Next reminder in " + str(hours) + " hr " + str(minutes) + "min"

# find port number of microbit
def find_microbit_comport():
	ports = list(list_ports.comports())
	for p in ports:
		if (p.pid == 516) and (p.vid == 3368):
			return str(p.device)

hours, minutes = 0,0 
og_hrs, og_mins = 0,0

# SET UP CONNECTION
ser = serial.Serial()
ser.baudrate = 115200
ser.port = find_microbit_comport()
ser.open()

# START OF GUI
app = App(title="pill dispenser")
Text(app, text="	", height = 2)
menu = Box(app, align="top", width="fill")

# APP TITLE
intro = Text(menu, text="Pill Dispenser", size=80, align="top")
Text(app, text="	", height = 1)

# ERROR HANDLING FOR DATA INPUT 
notification = Text(app, text = "", size=20)
notification.repeat(60000, counter)
notification.hide()

error_displayhr = Text(app, text = "hours cannot be more than 12", color = "red", size=40)
error_displayhr.hide()
error_displaymin = Text(app, text = "minutes cannot be more than 59", color = "red", size=40)
error_displaymin.hide()

# LAYOUTS
Text(app, text="	", height = 2)
timer_box = Box(app, layout="grid", align="top")

# INPUT OF VALUES
hour_input = TextBox(timer_box, width=3, grid=[2,2])
hour_input.text_size=40
Text(timer_box, text="hr", size = 50, width=3, grid=[3,2])

min_input = TextBox(timer_box, width=3, grid=[4,2])
min_input.text_size=40
Text(timer_box, text="min", size = 50, width=4, grid=[5,2])

# BUTTONS FOR ADJUSTING TIMER
reset_button = PushButton(timer_box, text = "reset", command=reset_timer, padx=25, pady=25, grid=[0,2])
reset_button.bg = "red"
reset_button.text_color = "white"
reset_button.text_size = 20
Text(timer_box, text="	", grid=[1,2])

send_button = PushButton(timer_box, text = "send", command=check_data, padx=25, pady=25, grid=[7,2])
send_button.bg = "green"
send_button.text_color = "white"
send_button.text_size = 20
Text(timer_box, text="", width=3, grid=[6,2])

# app.set_full_screen()
app.display()

