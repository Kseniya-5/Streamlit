import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def run(df):
    st.write('Посмотрим на загруженные исторические данные')
    st.dataframe(df)

    if st.checkbox("Показать гистограмму для городов"):
        st.subheader('Гистограмма')

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