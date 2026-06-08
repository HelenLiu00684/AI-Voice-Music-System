
import time

import state


# ============================================
# SERIAL SEND HELPER
# ============================================

def send_cmd(

    ser,

    lock,

    cmd

):

    with lock:

        ser.write(

            (cmd+"\n")

            .encode()

        )


# ============================================
# LED ENGINE
# ============================================

def drive_led(

    energy_list,

    ser,

    lock

):

    print(
        "LED ENGINE STARTED"
    )

    prev = 0

    for energy in energy_list:

        # ====================================
        # stop condition
        # ====================================

        if not state.led_running:

            print(
                "LED STOP"
            )

            send_cmd(

                ser,

                lock,

                "C"

            )

            return

        diff = energy - prev

        prev = energy

        print(

            f"ENERGY:{energy:.2f}",

            f"DIFF:{diff:.2f}"

        )

        # ====================================
        # clear previous frame
        # ====================================

        send_cmd(

            ser,

            lock,

            "C"

        )

        # ====================================
        # beat visualization
        # ====================================

        if diff > 0.35:

            send_cmd(

                ser,

                lock,

                "R4"

            )

        elif diff > 0.20:

            send_cmd(

                ser,

                lock,

                "R3"

            )

        elif diff > 0.10:

            send_cmd(

                ser,

                lock,

                "R2"

            )

        elif diff > 0.05:

            send_cmd(

                ser,

                lock,

                "R1"

            )

        else:

            # ====================================
            # energy meter
            # ====================================

            if energy < 0.10:

                send_cmd(

                    ser,

                    lock,

                    "B1"

                )

            elif energy < 0.20:

                send_cmd(

                    ser,

                    lock,

                    "G2"

                )

            elif energy < 0.35:

                send_cmd(

                    ser,

                    lock,

                    "Y3"

                )

            else:

                send_cmd(

                    ser,

                    lock,

                    "Y4"

                )

        time.sleep(
            0.08
        )

    send_cmd(

        ser,

        lock,

        "C"

    )
