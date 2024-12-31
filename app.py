import pandas as pd
import streamlit as st
from datetime import date
import dash

from data_processing import load_data, process_data

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
    st.set_page_config(layout="wide")
    # Применение пользовательского CSS
    st.markdown("""
    <style>
        .reportview-container {
            background-color: white;
        }
        .main {
            background-color: white;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #ffb347;
            padding: 2rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        /* Стили для кнопок */
        .stButton > button {
            background-color: #f5dfbf;
            color: #333;
            border: 1px solid #e0c9a6;
            border-radius: 3px;
            padding: 0.1rem 0.33rem;
            font-size: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #e0c9a6;
            border-color: #d1b894;
        }
        .stButton > button:active, .stButton > button.active {
            background-color: #d1b894;
            border-color: #c2a782;
        }

        /* Медиа-запрос для мобильных устройств */
        @media (max-width: 768px) {
            .stApp {
                padding: 1rem;
            }
            .stButton > button {
                padding: 0.07rem 0.17rem;
                font-size: 4px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

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

    # Инициализация состояния кнопок
    if 'button_state' not in st.session_state:
        st.session_state.button_state = "all (6м)"

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

        with col2:
            col1, col2, col3, col4 = st.columns(8)
            with col1:
                if st.button("3д", key="3d", help="Показать данные за последние 3 дня"):
                    st.session_state.button_state = "3д"
            with col2:
                if st.button("1н", key="1w", help="Показать данные за последнюю неделю"):
                    st.session_state.button_state = "1н"
            with col3:
                if st.button("1м", key="1m", help="Показать данные за последний месяц"):
                    st.session_state.button_state = "1м"
            with col4:
                if st.button("all (6м)", key="6m", help="Показать данные за последние 6 месяцев"):
                    st.session_state.button_state = "all (6м)"
            with col5:
            with col6:
            with col7:
            with col8:
            
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
            
            if not filtered_df.empty:    
                st.plotly_chart(create_heatmap(filtered_df), use_container_width=True)

    # Добавляем JavaScript для стилизации активной кнопки
    st.markdown(f"""
    <script>
        var buttons = document.querySelectorAll('.stButton button');
        buttons.forEach(function(button) {{
            if (button.innerText === '{st.session_state.button_state}') {{
                button.classList.add('active');
            }} else {{
                button.classList.remove('active');
            }}
        }});
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

