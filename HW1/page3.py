from page2 import *
import aiohttp
import asyncio
import pandas as pd
import datetime


async def fetch_temperature(session, city, API_KEY):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'}
    async with session.get('https://api.openweathermap.org/data/2.5/weather', params=params) as response:
        if response.status == 200:
            data = await response.json()
            return city, data['main']['temp'], data['main']['temp_min'], data['main']['temp_max']
        elif response.status == 401:
            error_data = await response.json()
            st.error(f"Ошибка: {error_data['message']}")
            return None
        else:
            print(f"Ошибка при запросе для города {city}: {response.status}")
            return None


async def get_temperatures(cities, API_KEY):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_temperature(session, city, API_KEY) for city in cities]
        results = await asyncio.gather(*tasks)

        # Фильтрация результатов: убираем None (ошибки)
        return [(city, temp_now, temp_min, temp_max) for (city, temp_now, temp_min, temp_max) in results if
                temp_now is not None]


async def main(data, API_KEY):
    cities = data['city'].unique()
    temperatures = await get_temperatures(cities, API_KEY)

    if not temperatures:
        return pd.DataFrame(
            columns=['city', 'temp_now', 'temp_min', 'temp_max'])

    current_temp_df = pd.DataFrame(data=temperatures, columns=['city', 'temp_now', 'temp_min', 'temp_max'])
    return current_temp_df


# Определение нормальности температуры
def anomal_season(data_now, seasonal_stats):
    month_map = {
        (1, 2, 12): 'winter',
        (3, 4, 5): 'spring',
        (6, 7, 8): 'summer',
        (9, 10, 11): 'autumn'
    }
    current_season = ''
    for months, season in month_map.items():
        if datetime.datetime.now().month in months:
            current_season = season
            break

    city_data = seasonal_stats[
        (seasonal_stats['city'] == data_now['city']) & (seasonal_stats['season'] == current_season)]
    if city_data.empty:
        return 0

    mean_temp = city_data['mean_temp'].iloc[0]
    std_dev = city_data['std_temp'].iloc[0]

    if (data_now['temp_now'] > mean_temp + 2 * std_dev) or (data_now['temp_now'] < mean_temp - 2 * std_dev):
        return 'Аномалия'
    else:
        return 'Норма'


def run(df):
    st.title(':blue[Мониторинг текущей температуры]')
    API_KEY = st.text_input('Введите Ваш API_KEY:')

    if API_KEY:
        current_temp = asyncio.run(main(df, API_KEY))
        if not current_temp.empty:
            st.markdown(
                f'**<p style="font-size: 20px;">Посмотрим на загруженные данные за {datetime.datetime.now().strftime("%d.%m.%Y")} </p>**',
                unsafe_allow_html=True)
            st.dataframe(current_temp)

            st.markdown(
                f'**<p style="font-size: 20px;">Посмотрим в каких городах сейчас аномальная температура</p>**',
                unsafe_allow_html=True)
            seasonal_stats = calculate_seasonal_stats(df)
            current_temp['anomal_season'] = current_temp[['city', 'temp_now']].apply(
                lambda x: anomal_season(x, seasonal_stats), axis=1)
            st.dataframe(current_temp)

            if st.checkbox('Построить интерактивный график'):
                selected_city = st.selectbox('Выберите город для отображения температуры:',
                                             current_temp['city'].unique())
                city_data = current_temp[current_temp['city'] == selected_city]

                if not city_data.empty:
                    # Создаем график
                    st.write('Создаем столбчатый график для отображения текущей температуры. Столбец цвета определяет, '
                             'является ли температура нормальной или аномальной. Используются разные цвета для аномальных '
                             'и нормальных значений.')
                    fig = px.bar(city_data, x='city', y='temp_now',
                                 title=f'Текущая температура в городе {selected_city}',
                                 labels={'temp_now': 'Температура (°C)', 'city': 'Город'},
                                 color='anomal_season',
                                 color_discrete_map={'Норма': 'blue', 'Аномалия': 'red'}
                                 )
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning('### Пожалуйста, введите ваш API_KEY')
