import pandas as pd
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
from fig_heatmap import create_heatmap

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
            padding: 0px;
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
            background-color: #ffb347;
            line-height: 24px;
            color: #666;
            margin-top: 0px;
            margin-bottom: 0px;
            font-weight: bold;
        }
    </style>
"""


# Основная функция приложения
def main():
    st.set_page_config(layout="centered" )
  # Устанавливаем стиль для увеличения ширины контейнера
    st.markdown(
    """ <style> .css-1y0tngm { max-width: 1200px; /* Задаем нужную ширину */ } </style> """,
    unsafe_allow_html=True,
    )
    st.markdown(
      """
                <style>
                 .block-container { padding: 0 !important; margin: 0 !important; } 
                 .element-container { padding: 0 !important; margin: 0 !important;} 
                
                .reportview-container .markdown-text-container {
                    font-family: monospace;
                }
                .sidebar .sidebar-content {
                    background-image: linear-gradient(#2e7bcf,#2e7bcf);
                    color: white;
                }
                .Widget>label {
                    color: white;
                    font-family: monospace;
                }
                [class^="st-b"]  {
                    color: white;
                    font-family: monospace;
                }
                .st-bb {
                    background-color: #ffb347;
                }
                .st-at {
                    background-color: #ffb347;
                }
                footer {
                    font-family: monospace;
                }
                .reportview-container .main footer, .reportview-container .main footer a {
                    color: #ffb347;
                }
                header .decoration {
                    background-image: none;
                }

                
                </style>
                """,
      unsafe_allow_html=True,
  )


   # st.markdown(body_style, unsafe_allow_html=True)
    
    # Заголовок
    st.markdown(header_style, unsafe_allow_html=True)
    st.markdown('<div class="title"><h1>Simulative</h1></div>', unsafe_allow_html=True)
    
    # Подзаголовок
    st.markdown(subheader_style, unsafe_allow_html=True)
    st.markdown('<div class="subheader"><h2>Дашборд по анализу Telegram-каналов</h2></div>', unsafe_allow_html=True)
    
    # Выбор канала
    channels_list = processed_data['posts']['channel_name'].unique()
    selected_channel = st.selectbox('Выберите канал:', channels_list)

    posts = processed_data['posts']
    subs = processed_data['subs']
    
    fig_posts = create_fig_posts_inds(posts, selected_channel)
    fig_subs = create_fig_subs_inds(subs, selected_channel)

    filtered_df = pd.DataFrame()

    with st.container():
        # Размещение графиков на одной строке
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_posts, use_container_width=True)
        with col2:
            st.plotly_chart(fig_subs, use_container_width=True)

    with st.container():
        # Размещение графиков на одной строке
        # Кнопки для выбора периода
        col1, col2 = st.columns(2)
        with col1:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("3д"):
                    filtered_df = posts[(posts.channel_name == selected_channel) &
                                        (pd.to_datetime(posts.date) >= date_ago('days', 2))]
            with col2:
                if st.button("1н"):
                    filtered_df = posts[(posts.channel_name == selected_channel) &
                                        (pd.to_datetime(posts.date) >= date_ago('weeks', 1))]
            with col3:
                if st.button("1м"):
                    filtered_df = posts[(posts.channel_name == selected_channel) &
                                        (pd.to_datetime(posts.date) >= date_ago('months', 1))]
            with col4:
                if st.button("all (6м)"):
                    filtered_df = posts[(posts.channel_name == selected_channel) &
                                        (pd.to_datetime(posts.date) >= date_ago('months', 6))]
                  
            if not filtered_df.empty:    
                st.plotly_chart(create_heatmap(filtered_df), use_container_width=True)
        with col2:
            st.write('col2')

     

if __name__ == "__main__":
    main()
