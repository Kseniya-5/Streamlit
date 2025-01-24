import streamlit as st
import pandas as pd


def main():
    # Настройка страницы
    st.set_page_config(page_title='Мое приложение', page_icon='🌟')
    # st.sidebar.header('Загрузка данных')
    st.sidebar.markdown(
        '**<p style="font-size: 25px;">Загрузка данных</p>**',
        unsafe_allow_html=True)
    data = st.sidebar.file_uploader('Загрузите CSV-файл', type=['csv'])

    if data is not None:
        df = pd.read_csv(data)

        st.sidebar.title('Навигация')
        page = st.sidebar.radio('Выберите страницу:',
                                ['Анализ исторических данных', 'Мониторинг текущей температуры'], index=None)

        if page == 'Анализ исторических данных':
            import page2
            page2.run(df)
        elif page == 'Мониторинг текущей температуры':
            import page3
            page3.run(df)
        else:
            import page1
            page1.run(df)

    else:
        st.title(
            ':blue[ДЗ1. Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API] :sunglasses: ##')
        st.warning('### Пожалуйста, загрузите файл с историческими данными')

if __name__ == "__main__":
    main()
