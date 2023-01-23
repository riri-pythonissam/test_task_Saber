import numpy as np
import pandas as pd
import streamlit as st
import requests
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as md


def get_assets():
    assets = []
    url = 'https://api.coincap.io/v2/assets'
    response = requests.request("GET", url)
    data_list = response.json().get('data')
    for data in data_list:
        assets.append(data.get('id'))

    return assets

def get_history(date_from, date_to, id, period):
    dates, price = [], []
    url = f'https://api.coincap.io/v2/assets/{id}/history?interval={period}&start={date_from}&end={date_to}'
    response = requests.request("GET", url)
    if response.status_code != 400:
        data_list = response.json().get('data')
        for data in data_list:
            dates.append(pd.to_datetime(data.get('time')/1e3,unit='s'))
            price.append(float(data.get('priceUsd')))
    else:
        st.write(response.json().get('error'))
    history = pd.DataFrame(data=price, index=dates,columns=['priceUsd'])

    return history

with st.container():
    col1, col2, col3, col4 = st.columns((1,1,1,1))
    with col1:
        asset = st.selectbox('Select an asset', get_assets())
    with col2:
        date_from = st.date_input(
            "Date from",
            datetime.date.today() - datetime.timedelta(days=3))
    with col3:
        date_to = st.date_input(
            "Date to",
            datetime.date.today())
    with col4:
            period = st.selectbox('Select a period', ('d1','h12', 'h6', 'h2', 'h1', 'm30', 'm15', 'm5', 'm1'))


data = get_history(time.mktime(date_from.timetuple())*1e3, time.mktime(date_to.timetuple())*1e3, asset, period)

with st.container():
    col1_1, col2_1, col3_1 = st.columns((1,8,1))
    with col2_1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d %H:%M'))
        ax.bar(data.index, data['priceUsd'], width=0.1, align='center')
        plt.xlabel('Date')
        plt.ylabel('Price in USD')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

