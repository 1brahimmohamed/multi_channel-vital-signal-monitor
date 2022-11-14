# Uses python3

import serial
import matplotlib.pyplot as plt
import streamlit as st
import random
import hydralit_components as hc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import csv

st.set_page_config(layout='wide', initial_sidebar_state='collapsed', )

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

menu_data = [
    {'id': "Data Acquisition", 'icon': "bi bi-activity", 'label': "Data Acquisition"},
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
    st.session_state["x_ctr"] = []
    st.session_state['X_Bar'] = []
    st.session_state["Range"] = []
    st.session_state['X_BAR_Summation'] = 0
    st.session_state['Range_Summation'] = 0
    st.session_state['X_BAR_Average'] = 0
    st.session_state['Range_Average'] = 0
    st.session_state['X_Bar_Upper_Limit'] = 0
    st.session_state['Range_Upper_Limit'] = 0
    st.session_state['X_Bar_Lower_Limit'] = 0
    st.session_state['Range_Lower_Limit'] = 0
    st.session_state.summation = 0
    st.session_state.avg = 0
    st.session_state.rangeList = []
    st.session_state.Range_var = 0

# To print ECG
ecg_data = []
with open("data//ecg.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    ecg_data.append(int(row[0]))
ecg_data = ecg_data[160:220]

while True:
    # ser = serial.Serial("COM9", 9600)
    # ser.close()
    # ser.open()

    if 'x' in st.session_state:
        # data = ser.readline()

        st.session_state.x.append(st.session_state.i)
        st.session_state.y.append(random.randint(0, 5))

        st.session_state.i += 1

        # I think there as some errors with this peace of code (mathemtically)
        if st.session_state.i % 3 == 0:

            j = st.session_state.i - 2
            for j in range(st.session_state.i):
                st.session_state.summation = st.session_state.summation + st.session_state.y[j]
                st.session_state.Range.append(st.session_state.y[j])

            st.session_state.Range_var = max(st.session_state.Range) - min(st.session_state.Range)
            avg = st.session_state.summation / 3

            st.session_state.X_Bar.append(avg)
            st.session_state.X_BAR_Summation = st.session_state.X_BAR_Summation + avg
            st.session_state.X_BAR_Average = st.session_state.X_BAR_Summation / \
                                             len(st.session_state.X_Bar)

            st.session_state.Range.append(st.session_state.Range_var)
            st.session_state.Range_Summation = st.session_state.Range_Summation + st.session_state.Range_var
            st.session_state.Range_Average = st.session_state.Range_Summation / \
                                             len(st.session_state.Range)

            st.session_state.X_Bar_Upper_Limit = st.session_state.X_BAR_Average + \
                                                 (1.023 * st.session_state.Range_Average)
            st.session_state.X_Bare_Lower_Limit = st.session_state.X_BAR_Average - \
                                                  (1.023 * st.session_state.Range_Average)

            st.session_state.Range_Upper_Limit = (
                    2.575 * st.session_state.Range_Average)

            st.session_state.x_ctr.append(len(st.session_state.X_Bar))
    else:
        st.warning('App is not running')

    if f"{menu_id}" == "Data Acquisition":
        t = np.linspace(0, max(st.session_state.x), len(st.session_state.x))
        # x_ecg = 5*np.sin(7*t)*np.sin(.5*t)*np.cos(3.25*t)*1/5*np.cos(.0000325*t) + .8
        x_ecg = np.tile(ecg_data, len(t))
        t = t/50
        x_eeg = .05*np.sin(700*t) + .02*np.sin(600*t) + 0.05

        fig_data = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02, x_title='<b>Time (S)</b>',
                            y_title='<b>Amplitude (mV)</b>')

        fig_data.add_trace(go.Scatter(x=np.array(st.session_state.x)/50, y=np.array(st.session_state.y), name='SPO2'),
                      row=1, col=1)
        fig_data.add_trace(go.Scatter(x=t, y=x_ecg, name='ECG'),
                      row=2, col=1)
        fig_data.add_trace(go.Scatter(x=t, y=x_eeg, name='EEG'),
                      row=3, col=1)
        fig_data.update_layout(margin=dict(l=60, r=0, t=0, b=50), font=dict(
            family="Sans serif",
            size=12), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), height=600,
                          width=600, title={
            'text': "<b>Data Acquisition</b>",
            'y':1.,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

        graph_placeholder.plotly_chart(fig_data, use_container_width=True)

    elif f"{menu_id}" == "Monitoring":
        fig, ax = plt.subplots(2, 1, figsize=(1,7))
        plt.style.use('ggplot')
        # plt.figure(figsize=(15, 40))

        # set the spacing between subplots
        # plt.subplots_adjust(wspace=1.)

        # I think there are some problems with x-bar formulas, I multiplied constants by array of ones to be able to
        # draw it as a constant number

        ax[0].plot(st.session_state.x_ctr, st.session_state.X_Bar_Upper_Limit*np.ones(len(st.session_state.X_Bar)),
                color='red', markersize=12)
        ax[0].plot(st.session_state.x_ctr, st.session_state.X_Bar,
                   color='black', markersize=12)
        ax[0].plot(st.session_state.x_ctr, st.session_state.X_BAR_Average*np.ones(len(st.session_state.X_Bar)),
                   color='green', markersize=12)
        ax[0].plot(st.session_state.x_ctr, st.session_state.X_Bare_Lower_Limit*np.ones(len(st.session_state.X_Bar)),
                   color='red', markersize=12)
        ax[0].set_title('Xbar-R Chart of Data', fontdict={'fontsize': 25})
        ax[0].set_xlabel('<b>Sample</b>')
        ax[0].set_ylabel('<b>Sample Range</b>')

        # Please type here the range equations
        ax[1].plot(st.session_state.x_ctr, st.session_state.X_Bar_Upper_Limit * np.ones(len(st.session_state.X_Bar)),
                   color='red', markersize=12)
        ax[1].plot(st.session_state.x_ctr, st.session_state.X_Bar,
                   color='black', markersize=12)
        ax[1].plot(st.session_state.x_ctr, st.session_state.X_BAR_Average * np.ones(len(st.session_state.X_Bar)),
                   color='green', markersize=12)
        ax[1].plot(st.session_state.x_ctr, st.session_state.X_Bare_Lower_Limit * np.ones(len(st.session_state.X_Bar)),
                   color='red', markersize=12)
        ax[1].set_xlabel('<b>Sample</b>')
        ax[1].set_ylabel('<b>Sample Range</b>')
        graph_placeholder.plotly_chart(fig, use_container_width=True)





