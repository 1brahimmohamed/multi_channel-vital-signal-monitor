# Uses python3

import serial
import matplotlib.pyplot as plt
import streamlit as st
from serial import Serial
import random
from streamlit_option_menu import option_menu

leftCol, rightCol = st.columns(2)

with st.sidebar:
    selected = option_menu("Main Menu", ["Data Acquisiton", 'Monitoring'],
                           icons=['house', 'gear'], menu_icon="cast", default_index=1)


if (selected == "Data Acquisiton"):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    i = 0
    j = 0
    x = list()
    y = list()

    # ser = serial.Serial("COM9", 9600)
    # ser.close()
    # ser.open()

    while True:
        # data = ser.readline()
        x.append(i)
        y.append(random.randint(0, 5))
        ymin = min(y)
        ymax = max(y)

        ax1.plot(x, y)
        ax1.set_ylim([ymin, ymax])
        st.write(fig)
        i += 1
        j += 1
        plt.pause(5)
