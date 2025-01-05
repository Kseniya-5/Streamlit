import streamlit as st


def main():
    # Настройка страницы
    st.set_page_config(page_title='Мое приложение', page_icon='🌟')

    st.sidebar.title('Навигация')
    page = st.sidebar.radio('Выберите страницу:',
                            ['Описание задания', 'Загрузка данных', 'Анализ исторических данных', 'Визуализация данных'])

    if page == 'Описание задания':
        import default
        default.run()
    elif page == 'Загрузка данных':
        import page1
        page1.run()
    elif page == 'Анализ исторических данных':
        import page2
        page2.run()
    elif page == 'Визуализация данных':
        import page3
        page3.run()



if __name__ == "__main__":
    main()
