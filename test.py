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
    st.session_state["i"] = 1
    st.session_state["x_ctr"] = []
    st.session_state['X_Bar'] = []
    st.session_state["Range"] = []
    st.session_state['X_BAR_Summation'] = 0
    st.session_state['Range_Summation'] = 0
    st.session_state['X_BAR_Average'] = 0
    st.session_state['Range_Average'] = 0
    st.session_state['X_Bar_Upper_Limit'] = []
    st.session_state['Range_Upper_Limit'] = []
    st.session_state['X_Bar_Lower_Limit'] = []
    st.session_state['Range_Lower_Limit'] = 0


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

        # I think there as some errors with this peace of code (mathemtically)
        if st.session_state.i % 3 == 0:
            summation = 0
            avg = 0
            rangeList = []
            Range = 0

            j = st.session_state.i - 2

            while j <= st.session_state.i:
                summation = summation + st.session_state.y[j-1]
                rangeList.append(st.session_state.y[j-1])
                j += 1

            Range = max(rangeList) - min(rangeList)
            avg = summation / 3

            # All Calculations are done here!
            st.session_state.X_Bar.append(avg)
            st.session_state.X_BAR_Summation = st.session_state.X_BAR_Summation + avg
            st.session_state.X_BAR_Average = st.session_state.X_BAR_Summation / \
                len(st.session_state.X_Bar)

            st.session_state.Range.append(Range)
            st.session_state.Range_Summation = st.session_state.Range_Summation + Range
            st.session_state.Range_Average = st.session_state.Range_Summation / \
                len(st.session_state.Range)

            st.session_state.X_Bar_Upper_Limit.append(st.session_state.X_BAR_Average +
                                                      (1.023 * st.session_state.Range_Average))
            st.session_state.X_Bar_Lower_Limit.append(st.session_state.X_BAR_Average -
                                                      (1.023 * st.session_state.Range_Average))

            st.session_state.Range_Upper_Limit.append((
                2.575 * st.session_state.Range_Average))

            st.session_state.x_ctr.append(len(st.session_state.X_Bar))

        st.session_state.i += 1
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
            'y': 1.,
            'x': 0.52,
            'xanchor': 'center',
            'yanchor': 'top'})

        graph_placeholder.plotly_chart(fig_data, use_container_width=True)
        plt.pause(1)

    elif f"{menu_id}" == "Monitoring":
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, x_title='<b>Time(S)</b>',
                            y_title='<b>XBar-Range</b>')

        # I think there are some problems with x-bar formulas, I multiplied constants by array of ones to be able to
        # draw it as a constant number

        fig.add_trace(go.Scatter(x=st.session_state.x_ctr,
                                 y=st.session_state.X_Bar, name='X_Bar', mode='lines + markers'), row=1, col=1)
        fig.add_trace(go.Scatter(x=st.session_state.x_ctr,
                                 y=st.session_state.X_Bar_Upper_Limit, name='X_Bar Upper Limit', line=dict(dash='dot')), row=1, col=1)
        fig.add_trace(go.Scatter(x=st.session_state.x_ctr,
                                 y=st.session_state.X_Bar_Lower_Limit, name='X_Bar Lower Limit', line=dict(dash='dot')), row=1, col=1)

        fig.add_trace(go.Scatter(x=st.session_state.x_ctr,
                                 y=st.session_state.Range, name='Range', mode='lines + markers'), row=2, col=1)
        fig.add_trace(go.Scatter(x=st.session_state.x_ctr,
                                 y=st.session_state.Range_Upper_Limit, name='Range Upper Limit', line=dict(dash='dot')), row=2, col=1)
        fig.update_layout(margin=dict(l=60, r=0, t=0, b=50), font=dict(
            family="Sans serif",
            size=12), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), height=600,
            width=600, title={
            'text': "<b>Monitoring</b>",
            'y': 1.,
            'x': 0.51,
            'xanchor': 'center',
            'yanchor': 'top'})
        graph_placeholder.plotly_chart(fig, use_container_width=True)

        i = len(st.session_state.x_ctr) - 1
        if(st.session_state.X_Bar[i] > st.session_state.X_Bar_Upper_Limit[i] or st.session_state.X_Bar[i] < st.session_state.X_Bar_Lower_Limit[i]):
            st.error("X_Bar is out of its Limits!!! Alarm will be set")
        if(st.session_state.Range[i] > st.session_state.Range_Upper_Limit[i] or st.session_state.Range[i] < 0):
            st.error("Range is out of its Limits!!! Alarm will be set")
        plt.pause(1)
