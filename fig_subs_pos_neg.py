import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def create_subs_pos_neg(subs, channel, date_range):
    if channel is None or date_range is None:
        st.write({})  # Вывод пустой фигуры
        return

    subdf_channel = subs[subs['channel_name'] == channel]

    # Проверяем, что дата присутствует и не пуста
    if len(subdf_channel) == 0 or 'datetime' not in subdf_channel.columns:
        st.write({})
        return

    # Преобразуем строку в datetime
    subdf_channel.loc[:, 'datetime'] = pd.to_datetime(subdf_channel['datetime'])
    start_time, end_time = date_range

    filtered_df = subdf_channel[(pd.to_datetime(subdf_channel['datetime']).dt.date >= start_time) & 
                                (pd.to_datetime(subdf_channel['datetime']).dt.date <= end_time)]

    # Преобразуем строку в datetime
    #subdf_channel.loc[:, 'datetime'] = pd.to_datetime(subdf_channel['datetime'])
    #start_time = subdf_channel['datetime'].min() + pd.Timedelta(seconds=slider_range[0])
    #end_time = subdf_channel['datetime'].min() + pd.Timedelta(seconds=slider_range[1])

    #filtered_df = subdf_channel[(subdf_channel['datetime'] >= start_time) & (subdf_channel['datetime'] <= end_time)]


    
    filtered_df_uniq = filtered_df[['date', 'day_change_pos', 'day_change_neg']].drop_duplicates()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_df_uniq['date'], y=filtered_df_uniq['day_change_pos'], 
                         marker_color='#F5DEB3', 
                         hovertemplate='%{x} <br>Подписались: %{y} <extra></extra>'))
    fig.add_trace(go.Bar(x=filtered_df_uniq['date'], y=filtered_df_uniq['day_change_neg'], 
                         marker_color='#8B0000', 
                         hovertemplate='%{x} <br>Отписались: %{y}<extra></extra>'))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor= '#ffb347',
        plot_bgcolor=  '#ffb347',
        font_family='Georgia',
        title_font_size=24,
        title_x=0.5,
        margin=dict(l=40, r=60, t=40, b=10),
        yaxis_title="Изменение подписок",
        xaxis_title="Дата и время",
        title = '',
        xaxis=dict(
            rangeselector=dict(
                bgcolor= '#f5dfbf',
                font=dict(color="#333"),
                activecolor= '#ffb347',
                bordercolor='#f5dfbf',                
                buttons=list([
                    dict(count=3, label="3д", step="day", stepmode="backward"),
                    dict(count=7, label="1н", step="day", stepmode="backward"),
                    dict(count=1, label="1м", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ))
    )
    return fig



def create_slider(subs, channel):
    if channel is None:
        return None

    subs = subs[subs['channel_name'] == channel]    
    # Получаем минимальную и максимальную дату
    date_min = pd.to_datetime(subs['datetime']).min().date()
    date_max = pd.to_datetime(subs['datetime']).max().date()

    
    selected_range = st.slider(
        'Выберите диапазон дат:',
        min_value=date_min,
        max_value=date_max,
        value=(date_min, date_max),
        format= "%Y-%M-%D"
    )
    
    return selected_range




    
