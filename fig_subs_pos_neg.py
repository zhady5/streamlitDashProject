import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def create_subs_pos_neg(subs, channel, slider_range):
    if channel is None or slider_range is None:
        st.write({})  # Вывод пустой фигуры
        return

    subdf_channel = subs[subs['channel_name'] == channel]

    # Проверяем, что дата присутствует и не пуста
    if len(subdf_channel) == 0 or 'datetime' not in subdf_channel.columns:
        st.write({})
        return

    # Преобразуем строку в datetime
    subdf_channel.loc[:, 'datetime'] = pd.to_datetime(subdf_channel['datetime'])
    start_time = subdf_channel['datetime'].min() + pd.Timedelta(seconds=slider_range[0])
    end_time = subdf_channel['datetime'].min() + pd.Timedelta(seconds=slider_range[1])

    filtered_df = subdf_channel[(subdf_channel['datetime'] >= start_time) & (subdf_channel['datetime'] <= end_time)]

    filtered_df_uniq = filtered_df[['date', 'day_change_pos', 'day_change_neg']].drop_duplicates()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_df_uniq['date'], y=filtered_df_uniq['day_change_pos'], marker_color='#F5DEB3', hovertemplate='%{x} <br>Подписались: %{y} <extra></extra>'))
    fig.add_trace(go.Bar(x=filtered_df_uniq['date'], y=filtered_df_uniq['day_change_neg'], marker_color='#8B0000', hovertemplate='%{x} <br>Отписались: %{y}<extra></extra>'))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor= '#ffb347', #'#FFFFFF',
        plot_bgcolor=  '#ffb347', #'#FFFFFF',
        font_family='Georgia',
        title_font_size=24,
        title_x=0.5,
        margin=dict(l=40, r=60, t=40, b=10),
        yaxis_title="Изменение подписок",
        xaxis_title="Дата и время",
        xaxis=dict(
            rangeselector=dict(  # Добавляем элементы управления диапазоном
                bgcolor= '#f5dfbf' ,  # Фоновый цвет области с кнопками
                font=dict(color="#333"),  # Цвет текста на кнопках
                activecolor= '#ffb347',  # Цвет активной кнопки
                bordercolor='#f5dfbf',  # Цвет рамки вокруг кнопок                
                buttons=list([
                    dict(count=3, label="3д", step="day", stepmode="backward"),
                    dict(count=7, label="1н", step="day", stepmode="backward"),
                    dict(count=1, label="1м", step="month", stepmode="backward"),
                    dict(step="all")  # Кнопка для просмотра всего диапазона
                ])
            )) 
    )
    return fig

def create_slider(subs, channel):
    if channel is None:
        st.write({})  # Вывод пустой фигуры
        return

    subs = subs[subs['channel_name'] == channel]    
     # Получаем минимальную и максимальную дату
    date_min = pd.to_datetime(subs['datetime']).min()
    date_max = pd.to_datetime(subs['datetime']).max()
    
    # Создаем интервал между минимальной и максимальной датой
    time_delta = (date_max - date_min).total_seconds()
    
    # Разделим временной промежуток на шаги для слайдера
    step = 86400 # секунд в одни сутки
    
    # Определяем начальные значения слайдера
    initial_value = [int(0), int(time_delta)]

    
    # Отображаем слайдер
    return st.slider(
                        'Выберите диапазон дат:',
                        min_value=int(0),
                        max_value=int(time_delta),
                        value=initial_value,
                        step=int(step)
                    )   

        # Функция для генерации меток
def generate_labels(subs):
    labels = []
    for date in pd.to_datetime(subs['datetime']):
        labels.append(st.markdown(f"**{date.strftime('%b %d, %H:%M')}**"))
    return labels

    
