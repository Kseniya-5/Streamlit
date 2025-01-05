import streamlit as st

def run():
    st.title('Шаг 1. Анализ исторических данных')

    if 'data' in st.session_state:
        data = st.session_state.data

        st.write('**1.1 Вычисляем скользящее среднее температуры с окном в 30 дней для сглаживания краткосрочных колебаний**')
        data['moving_avg'] = data.groupby('city')['temperature'].transform(
            lambda x: x.rolling(window=30, min_periods=1).mean())
        st.dataframe(data[['city', 'moving_avg']])


        st.write('**1.2 Рассчитываем среднюю температуру и стандартное отклонение для каждого сезона в каждом городе**')
        seasonal_stats = data.groupby(['city', 'season']).agg(mean_temp=('temperature', 'mean'),
                                                              std_temp=('temperature', 'std')).reset_index()
        st.dataframe(seasonal_stats)


        st.write('**1.3 Выявляем аномалии, где температура выходит за пределы _среднее_ ±2σ**')
        anomalies = seasonal_stats[(seasonal_stats['temperature'] < (seasonal_stats['mean_temp'] - 2 * seasonal_stats['std_temp'])) |
                         (seasonal_stats['temperature'] > (seasonal_stats['mean_temp'] + 2 * seasonal_stats['std_temp']))]
        st.dataframe(anomalies)


        st.write('**1.4 Распараллеливание анализа и сравнение скоростей выполнения**')
    else:
        st.write('Пожалуйста, загрузите данные на странице "Загрузка данных".')
