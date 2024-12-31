import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta


def create_subs_pos_neg(subs, channel): #, slider_range
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
        title = '',
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



def update_slider_marks(subs, channel):
    if channel is None:
        return {}

    subdf_channel = subs[subs["channel_name"] == channel]
    dates = sorted(subdf_channel["date"])

    # Преобразуем строки в даты
    dates = [
        datetime.strptime(str(date), "%Y-%m-%d") for date in dates
    ]

    date_min = min(dates)

    if len(dates) > 0:
        marks = {
            int((date - date_min).total_seconds()): {
                "label": date.strftime("%b %d"),
                "style": {
                    "fontSize": "12px",
                    "color": "black",
                    "backgroundColor": "#f5dfbf",
                    "borderRadius": "5px",
                    "padding": "2px",
                    "display": "block",
                    "width": "auto",
                    "transform": "translateX(-50%)",
                },
            }
            for date in dates[:: max(1, len(dates) // 6)]
        }
    else:
        marks = {}

    return marks

    
