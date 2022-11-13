# Uses python3

import serial
import matplotlib.pyplot as plt
import streamlit as st
from serial import Serial
import random
from streamlit_option_menu import option_menu
import hydralit_components as hc
import plotly.express as px

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

if "x" not in st.session_state:
    st.session_state["x"] = []
    st.session_state["y"] = []
    st.session_state["i"] = 0

if (f"{menu_id}" == "Data Acquisiton"):
    with leftCol:
        fig, ax = plt.subplots()

        # ser = serial.Serial("COM9", 9600)
        # ser.close()
        # ser.open()

        while True:
            # data = ser.readline()
            st.session_state.x.append(st.session_state.i)
            st.session_state.y.append(random.randint(0, 5))
            ymin = min(st.session_state.y)
            ymax = max(st.session_state.y)

            ax.plot(st.session_state.x, st.session_state.y,
                    color='blue', markersize=12)
            ax.set_ylim([ymin, ymax])
            graph_placeholder.plotly_chart(fig)
            st.session_state.i += 1

            plt.pause(1)

# if (f"{menu_id}" == "Monitoring"):
#     with leftCol:
#         fig = px
#         while True:
#         fig2 = px.histogram(st.session_state.x, st.session_state.y)
#         graph_placeholder.plotly_chart(fig2)
