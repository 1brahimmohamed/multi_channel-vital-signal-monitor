# Uses python3

import serial
import matplotlib.pyplot as plt
import streamlit as st
from serial import Serial
import random
from streamlit_option_menu import option_menu
import hydralit_components as hc

st.set_page_config(layout='wide', initial_sidebar_state='collapsed',)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

menu_data = [
    {'id': "Data Acquisiton", 'icon': "bi bi-activity", 'label': "Data Acquisiton"},
    {'id': 'Monitoring', 'icon': "bi bi-bar-chart-line-fill", 'label': "Monitoring"},
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    # will show the st hamburger as well as the navbar now!
    hide_streamlit_markers=False,
    use_animation=True,
    sticky_nav=True,  # at the top or not
    sticky_mode='pinned',  # jumpy or not-jumpy, but sticky or pinned
)

leftCol, rightCol = st.columns(2)
graph_placeholder = st.empty()

if (f"{menu_id}" == "Data Acquisiton"):
    with leftCol:
        fig, ax = plt.subplots()

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

            ax.plot(x, y, color='blue', markersize=12)
            ax.set_ylim([ymin, ymax])
            graph_placeholder.plotly_chart(fig)
            i += 1
            j += 1
            plt.pause(1)
