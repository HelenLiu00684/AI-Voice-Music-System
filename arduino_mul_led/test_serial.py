import serial
import time

PORT="COM3"

ser=serial.Serial(
    PORT,
    115200
)

time.sleep(2)

print("connected")

while True:

    cmd=input(
        "input cmd:"
    )

    ser.write(
        (cmd+"\n").encode()
    )

    print(
        "sent:",
        cmd
    )