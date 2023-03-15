def on_received_number(receivedNumber):
    global flag
    serial.write_string("0")
    flag = 0
    while True:
        music.play_tone(262, music.beat(BeatFraction.WHOLE))
        if input.magnetic_force(Dimension.STRENGTH) >= 800 and flag == 1:
            serial.write_string("1")
            # 1 means taken
            flag = 0
            break
        if input.magnetic_force(Dimension.STRENGTH) < 800:
            if serial.read_string() == "3":
                break
            flag = 1
radio.on_received_number(on_received_number)

flag = 0
music.set_volume(30)
radio.set_group(1)