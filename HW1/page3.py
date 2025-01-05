import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title('Визуализация данных')
    if 'data' in st.session_state:
        data = st.session_state.data
        st.subheader('Гистограмма')
        column = st.selectbox('Выберите колонку для гистограммы', data.columns)
        bins = st.slider('Количество интервалов (bins)', 5, 50, 10)

        fig, ax = plt.subplots()
        ax.hist(data[column], bins=bins, color='skyblue', edgecolor='black')
        st.pyplot(fig)


    else:
        st.write('Пожалуйста, загрузите данные на странице "Загрузка данных".')