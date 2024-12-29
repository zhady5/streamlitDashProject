import streamlit as st
from datetime import date
import dash

from data_processing import  load_data, process_data

from functions import date_ago, convert_date, get_gradient_color, get_current_previous_sums, create_table, hex_to_rgb\
                            , interpolate_color, gradient_color_func \
                        , calculate_mean_max_subs, calculate_mean_posts, calculate_mean_views, calculate_mean_reacts\
                        , load_stopwords_from_file

from fig_posts_inds import create_fig_posts_inds
from fig_subs_inds import create_fig_subs_inds

channels, posts, reactions, subscribers, views = load_data()
processed_data = process_data(channels, posts, reactions, subscribers, views)

# Стили заголовков и подзаголовков
header_style = """
    <style>
        .title h1 {
            font-family: 'Open Sans', sans-serif;
            font-size: 28px;
            line-height: 36px;
            color: #333;
            background-color: #ffb347;
            padding: 20px;
            box-shadow: 0 10px 15px rgba(0,0,0,0.05);
            border-radius: 10px;
            text-align: center;
        }
    </style>
"""

subheader_style = """
    <style>
        .subheader h2 {
            font-family: 'Open Sans', sans-serif;
            font-size: 16px;
            line-height: 24px;
            color: #666;
            margin-top: 20px;
            margin-bottom: 20px;
            font-weight: bold;
        }
    </style>
"""


# Основная функция приложения
def main():
    st.set_page_config(layout="wide")
    
    # Заголовок
    st.markdown(header_style, unsafe_allow_html=True)
    st.markdown('<div class="title"><h1>Simulative</h1></div>', unsafe_allow_html=True)
    
    # Подзаголовок
    st.markdown(subheader_style, unsafe_allow_html=True)
    st.markdown('<div class="subheader"><h2>Дашборд по анализу Telegram-каналов</h2></div>', unsafe_allow_html=True)
    
    # Выбор канала
    channels = posts['channel_name'].unique()
    selected_channel = st.selectbox('Выберите канал:', channels)
    
    fig_posts = create_fig_posts_inds(posts, selected_channel)
    fig_subs = create_fig_subs_inds(subs, selected_channel)
        # Размещение графиков на одной строке
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_posts, use_container_width=True)
    with col2:
        st.plotly_chart(fig_subs, use_container_width=True)

if __name__ == "__main__":
    main()
