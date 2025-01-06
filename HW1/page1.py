import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def run(df):
    st.title(
        ':blue[ДЗ1. Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API] :sunglasses:')
    st.markdown(
        '**<p style="font-size: 20px;">Посмотрим на загруженные исторические данные</p>**',
        unsafe_allow_html=True)
    count = range(1, len(df) + 1)
    selected_count = st.selectbox('Выберите количество строк', count)
    st.dataframe(df.head(selected_count))

    if st.checkbox("Показать гистограмму температур для городов"):
        st.subheader('Гистограмма температур')

        # Получаем уникальные города
        cities = df['city'].unique()
        selected_city = st.selectbox('Выберите город', cities)  #
        city_data = df[df['city'] == selected_city]['temperature']

        bins = st.slider('Количество интервалов (bins)', 5, 50, 10)

        fig, ax = plt.subplots()
        ax.hist(city_data, bins=bins, color='skyblue', edgecolor='black')

        ax.set_title(f'Гистограмма температур для города {selected_city}', fontsize=16)
        ax.set_xlabel('Температура (°C)', fontsize=14)
        ax.set_ylabel('Частота', fontsize=14)

        st.pyplot(fig)

    return 1
