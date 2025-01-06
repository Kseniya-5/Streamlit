import streamlit as st
import pandas as pd


def main():
    # Настройка страницы
    st.set_page_config(page_title='Мое приложение', page_icon='🌟')
    st.markdown(
        '## :blue[ДЗ1. Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API] :sunglasses: ##')
    st.sidebar.header('Загрузка данных')
    data = st.sidebar.file_uploader('Загрузите CSV-файл', type=['csv'])
    flag = 0
    if data is not None:
        df = pd.read_csv(data)
        if flag == 0:
            import page1
            flag = page1.run(df)

        if flag == 1:
            st.sidebar.title('Навигация')
            page = st.sidebar.radio('Выберите страницу:',
                                    ['Загрузка данных', 'Анализ исторических данных', 'Визуализация данных'])

            if page == 'Анализ исторических данных':
                import page2
                page2.run()
            elif page == 'Визуализация данных':
                import page3
                page3.run()
    else:
        st.warning('### Пожалуйста, загрузите файл с историческими данными ###')


if __name__ == "__main__":
    main()
