# Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API

Ссылка на приложение https://pythonprojects-wdafjj6kxhkvmzxsxy9nl7.streamlit.app/

## Стартовая страница
![image](https://github.com/user-attachments/assets/332b8798-9ec0-49fe-b535-e2a60be36f8e)

### После загрузки CSV-файла стартовая страница выглядит так:
Здесь можно выбрать количество строк для отображения и нарисовать гистограмму температур для каждого города с изменением интервала.
![image](https://github.com/user-attachments/assets/40b4a66c-c146-4f29-9ea5-68a09bebf46e)
![image](https://github.com/user-attachments/assets/226ba9a9-3e7f-4785-a157-323fe2cfc883)

## Анализ исторических данных
![image](https://github.com/user-attachments/assets/027e79af-6047-4e15-af01-99869f2cdea2)
На данной странице можно выбрать город для просмотра информации и открыть интерактивные графики

### Описательная статистика
![image](https://github.com/user-attachments/assets/34cc0ebd-9394-4f6f-b1d0-ee05a6b9f4c4)

### Вычисление сколзящей средней температуры (moving_avg) с окном в 30 дней
![image](https://github.com/user-attachments/assets/c65ffa64-9de9-452f-a634-cd5d3b1f53fe)

### Расчет средней температуры и стандартного отклонения для каждого сезона
Тут можно выбрать сезон, для которого будут построены графики ниже
![image](https://github.com/user-attachments/assets/0228dc48-58bb-4629-859a-1d2e9be5a03a)

### Выявляем аномалии, где температура выходит за пределы среднее ±2σ для каждого сезона
![image](https://github.com/user-attachments/assets/82b1f9a3-6847-41fc-92b2-312d6af0bded)

## Мониторинг текущей температуры
Пока не будет введет корректно API ключ, ничего показываться не будет
![image](https://github.com/user-attachments/assets/64f94da6-bb4d-4cf1-893c-21c7b905a0c3)
![image](https://github.com/user-attachments/assets/546b2085-044e-4d85-a661-fb3ce7fae018)

После корректного ввода API ключа, можно увидеть следующие данные на текущий день:
![image](https://github.com/user-attachments/assets/be704c5c-213b-4ecd-8bc4-80dc776ec552)

Также можно построить интерактивный график. Так как на 06.01.2025 аномалий нет, на графике будет показываться только текущая температура
![image](https://github.com/user-attachments/assets/1650e81e-8eb5-4273-82b7-54d2e7a0c513)



