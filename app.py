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
        .custom-button {
            background-color: #f5dfbf;
            color: #333;
            border: 1px solid #e0c9a6;
            border-radius: 0;
            padding: 2px 6px;
            font-size: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-right: -1px;
            cursor: pointer;
        }
        .custom-button:first-child {
            border-top-left-radius: 3px;
            border-bottom-left-radius: 3px;
        }
        .custom-button:last-child {
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
        .custom-button:hover {
            background-color: #e0c9a6;
            border-color: #d1b894;
        }
        .custom-button.active {
            background-color: #d1b894;
            border-color: #c2a782;
            z-index: 1;
        }
        
        /* Стили для контейнера кнопок */
        .button-container {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 10px;
        }
        
        /* Медиа-запрос для мобильных устройств */
        @media (max-width: 768px) {
            .stApp {
                padding: 1rem;
            }
            .custom-button {
                padding: 1px 3px;
                font-size: 8px;
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

    # Размещение графиков на одной строке
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_posts, use_container_width=True)
    with col2:
        st.plotly_chart(fig_subs, use_container_width=True)
        
        # Кнопки для выбора периода
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        for period, label in [("3д", "3д"), ("1н", "1н"), ("1м", "1м"), ("all (6м)", "all (6м)")]:
            button_class = "custom-button active" if st.session_state.button_state == period else "custom-button"
            st.markdown(f'<button class="{button_class}" onclick="handleButtonClick(\'{period}\')">{label}</button>', unsafe_allow_html=True)
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

    # Добавляем JavaScript для обработки кликов по кнопкам и обновления состояния
    st.markdown("""
    <script>
    function handleButtonClick(period) {
        // Обновляем состояние кнопок
        var buttons = document.querySelectorAll('.custom-button');
        buttons.forEach(function(button) {
            button.classList.remove('active');
            if (button.innerText === period) {
                button.classList.add('active');
            }
        });
        
        // Отправляем событие в Streamlit
        var event = new CustomEvent('streamlit:buttonClicked', { detail: period });
        window.dispatchEvent(event);
    }

    // Слушаем события от Streamlit
    window.addEventListener('streamlit:render', function(event) {
        var buttons = document.querySelectorAll('.custom-button');
        buttons.forEach(function(button) {
            if (button.innerText === '""" + st.session_state.button_state + """') {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    });
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

