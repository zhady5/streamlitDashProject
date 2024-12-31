import pandas as pd
import streamlit as st
from datetime import date
import dash

from data_processing import load_data, process_data
from functions import date_ago, convert_date, get_gradient_color, get_current_previous_sums, create_table, hex_to_rgb, \
    interpolate_color, gradient_color_func, calculate_mean_max_subs, calculate_mean_posts, calculate_mean_views, \
    calculate_mean_reacts, load_stopwords_from_file
from fig_posts_inds import create_fig_posts_inds
from fig_subs_inds import create_fig_subs_inds
from fig_heatmap import create_heatmap

channels, posts, reactions, subscribers, views = load_data()
processed_data = process_data(channels, posts, reactions, subscribers, views)

st.set_page_config(layout="wide")
# Стили заголовков и подзаголовков
st.markdown("""
<style>
    .title h1 {
        font-family: 'Open Sans', sans-serif;
        font-size: 28px;
        line-height: 36px;
        color: #333;
        background-color: #ffb347;
        padding: 0px;
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
        border-radius: 10px;
        text-align: center;
    }
    .subheader h2 {
        font-family: 'Open Sans', sans-serif;
        font-size: 16px;
        background-color: #ffb347;
        line-height: 24px;
        color: #666;
        margin-top: 0px;
        margin-bottom: 0px;
        font-weight: bold;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #ffb347;
        padding: 2rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .button-container {
        display: flex;
        justify-content: flex-start;
        gap: 1px;
        margin-bottom: 10px;
    }
    .stButton > button {
        background-color: #f5dfbf;
        color: #333;
        border: 1px solid #e0c9a6;
        border-radius: 3px;
        padding: 0px 0px;
        font-size: 6px;
        font-weight: 400;
    }
    .stButton > button:hover {
        background-color: #e0c9a6;
        border-color: #d1b894;
    }
    .stButton > button:active {
        background-color: #d1b894;
        border-color: #c2a782;
    }
</style>
""", unsafe_allow_html=True)

def main():
    

    # Заголовок
    st.markdown('<div class="title"><h1>Simulative</h1></div>', unsafe_allow_html=True)
    
    # Подзаголовок
    st.markdown('<div class="subheader"><h2>Дашборд по анализу Telegram-каналов</h2></div>', unsafe_allow_html=True)
    
    # Выбор канала
    channels_list = processed_data['posts']['channel_name'].unique()
    selected_channel = st.selectbox('Выберите канал:', channels_list)

    posts = processed_data['posts']
    subs = processed_data['subs']
    
    fig_posts = create_fig_posts_inds(posts, selected_channel)
    fig_subs = create_fig_subs_inds(subs, selected_channel)

    # Инициализация состояния кнопок
    if 'button_state' not in st.session_state:
        st.session_state.button_state = "all (6м)"

    # Размещение графиков на одной строке
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_posts, use_container_width=True)
    with col2:
        st.plotly_chart(fig_subs, use_container_width=True)
        
        # Кнопки для выбора периода
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12   = st.columns(12)
        with col1:
            if st.button("3д", key="3d"):
                st.session_state.button_state = "3д"
        with col2:
            if st.button("1н", key="1w"):
                st.session_state.button_state = "1н"
        with col3:
            if st.button("1м", key="1m"):
                st.session_state.button_state = "1м"
        with col4:
            if st.button("all (6м)", key="6m"):
                st.session_state.button_state = "all (6м)"
        with col5:
            st.empty()
        with col6:
            st.empty()   
        with col7:
            st.empty()
        with col8:
            st.empty()   
        with col9:
            st.empty()
        with col10:
            st.empty()   
        with col11:
            st.empty()
        with col12:
            st.empty()              
        st.markdown('</div>', unsafe_allow_html=True)

        # Фильтрация данных в зависимости от выбранной кнопки
        if st.session_state.button_state == "3д":
            filtered_df = posts[(posts.channel_name == selected_channel) &
                                (pd.to_datetime(posts.date) >= date_ago('days', 2))]
        elif st.session_state.button_state == "1н":
            filtered_df = posts[(posts.channel_name == selected_channel) &
                                (pd.to_datetime(posts.date) >= date_ago('weeks', 1))]
        elif st.session_state.button_state == "1м":
            filtered_df = posts[(posts.channel_name == selected_channel) &
                                (pd.to_datetime(posts.date) >= date_ago('months', 1))]
        else:  # "all (6м)"
            filtered_df = posts[(posts.channel_name == selected_channel) &
                                (pd.to_datetime(posts.date) >= date_ago('months', 6))]

        # Отображение тепловой карты
        st.plotly_chart(create_heatmap(filtered_df), use_container_width=True)

if __name__ == "__main__":
    main()

