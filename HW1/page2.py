import streamlit as st
import plotly.express as px
import numpy as np


# Функция для вычисления среднего и стандартного отклонения для города
def calculate_seasonal_stats(df):
    return df.groupby(['city', 'season']).agg(mean_temp=('temperature', 'mean'),
                                              std_temp=('temperature', 'std')).reset_index()


def run(df):
    st.title(':blue[Анализ исторических данных]')

    # Смотрим данные по определенному городу
    cities = df['city'].unique()
    selected_city = st.selectbox('Выберите город', cities)
    city_data = df[df['city'] == selected_city]
    st.markdown(
        '**<p style="font-size: 20px;">Описательная статистика</p>**',
        unsafe_allow_html=True)
    st.dataframe(city_data.describe())

    if st.checkbox('Построить интерактивный график для описательной статистики'):
        st.write('График отображает значения для каждого статистического показателя.')
        descriptive_stats = city_data.describe().reset_index().melt(id_vars='index', var_name='Statistic',
                                                                    value_name='Value')
        fig_descriptive = px.bar(descriptive_stats, x='index', y='Value', color='Statistic',
                                 title=f'Описательная статистика для {selected_city}',
                                 labels={'index': 'Показатели', 'Value': 'Значение'},
                                 template='plotly_white')
        st.plotly_chart(fig_descriptive, use_container_width=True)

    st.markdown(
        '**<p style="font-size: 20px;">Вычисляем сколзящее среднее температуры (moving_avg) с окном в 30 дней</p>**',
        unsafe_allow_html=True)
    city_data['moving_avg'] = city_data.groupby('city')['temperature'].transform(
        lambda x: x.rolling(window=30, min_periods=1).mean())
    st.dataframe(city_data)

    if st.checkbox('Построить интерактивный график для сколзящей средней температуры'):
        st.write('График показывает скользящее среднее и фактические температуры.')
        # Создаем интерактивный график
        fig = px.line(city_data, x='timestamp', y='moving_avg',
                      title=f'Скользящее среднее температуры в {selected_city}',
                      labels={'moving_avg': 'Скользящее среднее', 'timestamp': 'Дата'},
                      template='plotly_white')

        # Добавляем линию для фактических значений температуры
        fig.add_scatter(x=city_data['timestamp'], y=city_data['temperature'], mode='lines',
                        name='Температура', line=dict(color='orange', width=0.5))
        # Добавляем обозначение для moving_avg
        fig.add_scatter(x=city_data['timestamp'], y=city_data['moving_avg'], mode='lines',
                        name='Скользящее среднее', line=dict(color='blue', width=2))

        # Обновляем настройки графика
        fig.update_layout(yaxis_title='Температура (°C)', xaxis_title='Дата')

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '**<p style="font-size: 20px;">Расчет средней температуры и стандартного отклонения для каждого сезона</p>**',
        unsafe_allow_html=True)
    # Смотрим данные по определенному сезону
    seasons = ['winter', 'spring', 'summer', 'autumn']
    selected_season = st.selectbox('Выберите сезон', seasons)
    season_filter = city_data['season'] == selected_season
    season_data = city_data[season_filter]

    seasonal_stats = calculate_seasonal_stats(season_data)
    st.dataframe(seasonal_stats)

    if st.checkbox('Построить интерактивный график для ср. температуры и стандартного отклонения'):
        st.write('Каждое значимое значение сезона представлено столбцом, который отображает среднюю температуру.'
                 'Стандартное отклонение отображается в виде "ошибки" или "тени" '
                 'на верхней части столбца, показывая диапазон, в пределах которого данные могут колебаться.')
        fig_seasonal = px.bar(seasonal_stats, x='season', y='mean_temp',
                              error_y='std_temp',
                              title=f'Средняя температура и стандартное отклонение для {selected_city} в {selected_season}',
                              labels={'mean_temp': 'Средняя температура (°C)', 'season': 'Сезон'},
                              template='plotly_white')
        st.plotly_chart(fig_seasonal, use_container_width=True)

    st.markdown(
        '**<p style="font-size: 20px;">Выявляем аномалии, где температура выходит за пределы  среднее ±2σ</p>**',
        unsafe_allow_html=True)

    # Объединение данных с расчетами для определения аномалий
    city_data = city_data.merge(seasonal_stats, on=['city', 'season'])
    # Находим аномальные температуры (более чем 2 стандартных отклонения от среднего)
    city_data['is_anomaly'] = np.where(
        (city_data['temperature'] > (city_data['mean_temp'] + 2 * city_data['std_temp'])) |
        (city_data['temperature'] < (city_data['mean_temp'] - 2 * city_data['std_temp'])),
        True,
        False
    )
    # Выводим строки, где температура является аномальной
    anomalies = city_data[city_data['is_anomaly']]
    st.dataframe(anomalies[['city', 'timestamp', 'temperature', 'season', 'mean_temp', 'std_temp']])

    if st.checkbox('Построить интерактивный график для выявления аномалий'):
        st.write('График показывает температуры по всем дням для выбранного города, выделяя аномальные значения: \n'
                 '- **Аномалия**: температура, выходящая за пределы ±2 стандартных отклонения от средней.\n'
                 '- **Норма**: температуры, которые находятся в пределах нормального диапазона.')
        fig_anomaly = px.scatter(city_data, x='timestamp', y='temperature',
                                 color='is_anomaly',
                                 color_discrete_map={'Аномалия': 'red', 'Норма': 'blue'},
                                 title=f'Временной ряд температур в {selected_city} с аномалиями',
                                 labels={'temperature': 'Температура (°C)', 'timestamp': 'Дата'},
                                 template='plotly_white')

        fig_anomaly.add_scatter(x=city_data['timestamp'], y=city_data['mean_temp'], mode='lines',
                                name='Средняя температура', line=dict(color='green'))
        fig_anomaly.add_scatter(x=city_data['timestamp'], y=city_data['mean_temp'] + 2 * city_data['std_temp'],
                                mode='lines', name='Среднее + 2σ', line=dict(color='red', dash='dash'))
        fig_anomaly.add_scatter(x=city_data['timestamp'], y=city_data['mean_temp'] - 2 * city_data['std_temp'],
                                mode='lines', name='Среднее - 2σ', line=dict(color='red', dash='dash'))

        st.plotly_chart(fig_anomaly, use_container_width=True)
