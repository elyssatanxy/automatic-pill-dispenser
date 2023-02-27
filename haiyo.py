from guizero import App, Text, PushButton
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
    print(send_this)
    
    try:
        ser.write(send_this.encode())
    except SerialException:
        info("Error", "Could not send.")
        
        
# increment timer value
def increment_timer():
    global timer
    timer += 1
    print("updated timer to", timer)


# decrement timer value
def decrement_timer():
    global timer
    timer -= 1
    print("updated timer to", timer)


# TODO: stop and reset the timer immediately
def reset_timer():
    pass


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
timer = 3

app = App(title="pill dispenser")

intro = Text(app, text = "test")

# NOTE: these buttons will be removed to avoid any tampering
connect_btn = PushButton(app, text = "Connect", command=connect)
disconnect_button = PushButton(app, text = "Disconnect", command=disconnect)

# BUTTONS FOR ADJUSTING TIMER
increment_button = PushButton(app, text = "+", command=increment_timer)
decrement_button = PushButton(app, text = "-", command=decrement_timer)
send_btn = PushButton(app, text="Send", command=send_data)

# TODO: gui does not reflect the changes in timer values
timer_text = Text(app, text = timer)

app.display()