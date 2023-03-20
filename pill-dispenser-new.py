from guizero import App, Box, info, Text, TextBox, PushButton
import serial
from serial.serialutil import SerialException
from serial.tools import list_ports

# check data 
def check_data():
    global hour_input, min_input, hours, minutes, og_hrs, og_mins
    
    invalid_input = False
    error_displaymin_max.hide()
    error_displaymin_min.hide()
    error_displayhr_min.hide()
    error_hournan.hide()
    error_minnan.hide()
    
    if(len(hour_input.value) == 0):
        hours = 0
        og_hrs = 0
        error_displayhr_min.hide()
    else:
        try:
            if (int(hour_input.value) < 0):
                invalid_input = True
                error_displayhr_min.show()
            else:                               
                hours = int(hour_input.value)
                og_hrs = int(hour_input.value)
                error_displayhr_min.hide()
        except ValueError:
            invalid_input = True
            error_hournan.show()
            
    if(len(min_input.value) == 0):
        minutes = 0
        og_mins = 0
        error_displaymin_max.hide()
        error_displaymin_min.hide()
    else:
        try:
            if (int(min_input.value) > 59):
                invalid_input = True
                error_displaymin_max.show()
            elif (int(min_input.value) < 0):
                invalid_input = True
                error_displaymin_min.show()
            else:
                minutes = int(min_input.value)
                og_mins = int(min_input.value)
                error_displaymin_max.hide()
                error_displaymin_min.hide()
        except ValueError:
            invalid_input = True
            error_minnan.show()
        
    if(not invalid_input):             
        send_data()

# send number for timer
def send_data():
    global notification, hours, minutes
    
    seconds = (hours * 60 * 60) + (minutes) # minutes * 60
    send_this = str(seconds) + "\n"    
    
    try:
        print("sending value: " + str(hours) + " hr " + str(minutes) + " min = " + str(seconds) + "s" )
        ser.write(send_this.encode())
        if(seconds > 0):
            notification.value = "Next reminder in " + str(hours) + " hr " + str(minutes) + " min."
            notification.show()
        else:
            notification.value = "Timer reset to 0."
            notification.show()
            
    except SerialException:
        info("Error", "Could not send.")
    
    
# stop and reset the timer immediately
def reset_timer():
    global hours, minutes
    
    error_displayhr_min.hide()
    error_displaymin_max.hide()
    error_displaymin_min.hide()
    min_input.clear()
    hour_input.clear()
    
    hours = 0
    minutes = 0
    
    send_data()
    print("timer reset to 0")


# countdown timer
def counter():
    global hours, minutes, og_hrs, og_mins
    print(hours)
    print(minutes)
    if minutes < 0 or hours < 0:
        notification.value = "Invalid input, check if value of minutes or hours is negative."
    elif ((minutes - 1) == -1):
        hours -= 1
        minutes = 59
    elif ((hours - 1) == -1):
        hours = og_hrs
        minutes = og_mins
    else:
        minutes -= 1
        
    notification.value = "Next reminder in " + str(hours) + " hr " + str(minutes) + "min."


# find port number of microbit
def find_microbit_comport():
	ports = list(list_ports.comports())
	for p in ports:
		if (p.pid == 516) and (p.vid == 3368):
			return str(p.device)


hours, minutes = 0, 0 
og_hrs, og_mins = 0, 0


# SET UP CONNECTION
ser = serial.Serial()
ser.baudrate = 115200
ser.port = find_microbit_comport()
ser.open()


# START OF GUI
app = App(title="PillPal")
Text(app, text="	", height = 2)
menu = Box(app, align="top", width="fill")


# APP TITLE
intro = Text(menu, text="PillPal", size=80, align="top")
Text(app, text="	", height = 1)


# ERROR HANDLING FOR DATA INPUT 
notification = Text(app, text = "", size=20)
notification.hide()

error_displayhr_min = Text(app, text = "Hours cannot be negative.", color = "red", size=40)
error_displayhr_min.hide()
error_displaymin_max = Text(app, text = "Minutes cannot be more than 59.", color = "red", size=40)
error_displaymin_max.hide()
error_displaymin_min = Text(app, text = "Minutes cannot be negative.", color = "red", size=40)
error_displaymin_min.hide()

error_hournan = Text(app, text = "Hour value was not a number.", color = "red", size = 40)
error_hournan.hide()
error_minnan = Text(app, text = "Minute value was not a number.", color = "red", size = 40)
error_minnan.hide()


# LAYOUTS
Text(app, text="	", height = 2)
timer_box = Box(app, layout="grid", align="top")


# INPUT OF VALUES
hour_input = TextBox(timer_box, width=3, grid=[2,2])
hour_input.text_size = 40
Text(timer_box, text="hr", size = 50, width=3, grid=[3,2])

min_input = TextBox(timer_box, width=3, grid=[4,2])
min_input.text_size = 40
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

