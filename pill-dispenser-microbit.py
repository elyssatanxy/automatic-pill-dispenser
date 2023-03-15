def move_motor():
    pins.servo_write_pin(AnalogPin.P0, 0)
    basic.pause(200)
    pins.servo_write_pin(AnalogPin.P0, 90)

def on_data_received():
    global t, reset_stat, max_t
    t = int(serial.read_line())
    if t == 0:
        reset_stat = True
    else:
        reset_stat = False
    max_t = t
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)

reset_stat = False
max_t = 0
t = 0
t = max_t
reset_stat = True
radio.set_group(1)
serial.redirect_to_usb()
basic.show_string("A")

def on_forever():
    global t
    if reset_stat:
        basic.show_string("A")
    else:
        if t != 0:
            basic.show_number(t)
            t += 0 - 1
        if t == 0 and not reset_stat:
            t = max_t
            move_motor()
            radio.send_number(0)
        basic.pause(1000)
basic.forever(on_forever)