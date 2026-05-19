# led_engine.py

import time
import state


# ============================================
# REACTIVE LED ENGINE
# ============================================
#
# This module converts audio energy data
# into real-time LED behavior.
#
# Pipeline:
#
# audio energy
#     →
# threshold analysis
#     →
# beat-like change detection
#     →
# serial LED command
#     →
# Arduino hardware response
#
# IMPORTANT:
# This is NOT true DSP beat detection.
#
# Current implementation:
#     simplified energy-reactive lighting
#
# ============================================

def drive_led(energy_list, ser):

    """
    Drive Arduino LED behavior using
    analyzed audio energy data.
    """

    # ====================================
    # PREVIOUS ENERGY
    # ====================================
    #
    # Used for simple energy-difference
    # detection to simulate beat response.
    #
    # ====================================

    previous = 0

    # ====================================
    # MAIN REACTIVE LOOP
    # ====================================

    while state.music_playing:

        for energy in energy_list:

            # stop immediately if music ends
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
            # STRONG ENERGY CHANGE
            # ====================================
            #
            # Simulated beat pulse
            #
            # R = red flash
            #
            # ====================================

            if diff > 0.30:

                ser.write(b'R')

                time.sleep(0.05)

            # ====================================
            # HIGH ENERGY
            # ====================================
            #
            # Y = yellow
            #
            # ====================================

            elif energy > 0.50:

                ser.write(b'Y')

                time.sleep(0.06)

            # ====================================
            # MID ENERGY
            # ====================================
            #
            # G = green
            #
            # ====================================

            elif energy > 0.20:

                ser.write(b'G')

                time.sleep(0.08)

            # ====================================
            # LOW ENERGY
            # ====================================
            #
            # B = blue
            #
            # ====================================

            else:

                ser.write(b'B')

                time.sleep(0.10)

            # ====================================
            # UPDATE PREVIOUS ENERGY
            # ====================================

            previous = energy