import serial
import time

ser=serial.Serial(
    "COM3",
    115200
)

time.sleep(2)

colors=["R","Y","G","B"]

while True:

    for c in colors:

        for level in range(1,5):

            cmd=f"{c}{level}"

            print(cmd)

            ser.write(
                (cmd+"\n").encode()
            )

            time.sleep(1)

    # full cycle finished

    for c in colors:

        cmd=f"{c}0"

        ser.write(
            (cmd+"\n").encode()
        )

    time.sleep(1)

