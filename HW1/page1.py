import streamlit as st
import pandas as pd


def run():
    st.title('Загрузка данных')
    uploaded_file = st.file_uploader('Загрузите CSV-файл с историческими данными', type=['csv'])

    # Кэшируем данные
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.session_state.data = data  # Сохраняем данные в session_state
        st.write('Посмотрим на загруженные данные')
        st.dataframe(data)

        if st.checkbox("Показать описательную статистику для числовой переменной"):
            st.write(data.describe())
    else:
        st.write('Пожалуйста, загрузите исторические данные.')
