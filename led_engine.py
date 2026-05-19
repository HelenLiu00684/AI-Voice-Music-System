import state
import time


def drive_led(energy_list, ser):

    previous = 0

    while state.music_playing:

        for energy in energy_list:

            if not state.music_playing:
                return

            # ====================================
            # ENERGY DIFFERENCE
            # ====================================

            diff = energy - previous

            print(
                "ENERGY:",
                round(energy, 2),
                "DIFF:",
                round(diff, 2)
            )

            # ====================================
            # STRONG BEAT DETECTED
            # ====================================

            if diff > 0.30:

                # RED FAST FLASH
                ser.write(b'R')

                time.sleep(0.08)

                ser.write(b'B')

                time.sleep(0.08)

            # ====================================
            # HIGH ENERGY
            # ====================================

            elif energy > 0.50:

                ser.write(b'Y')

                time.sleep(0.2)

            # ====================================
            # MID ENERGY
            # ====================================

            elif energy > 0.20:

                ser.write(b'G')

                time.sleep(0.25)

            # ====================================
            # LOW ENERGY
            # ====================================

            else:

                ser.write(b'B')

                time.sleep(0.3)

            previous = energy