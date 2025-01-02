import pandas as pd
import streamlit as st
from datetime import date

from data_processing import load_data, process_data
from functions import date_ago, convert_date, get_gradient_color, get_current_previous_sums,  hex_to_rgb, \
    interpolate_color, gradient_color_func, calculate_mean_max_subs, calculate_mean_posts, calculate_mean_views, \
    calculate_mean_reacts, load_stopwords_from_file
from fig_posts_inds import create_fig_posts_inds
from fig_subs_inds import create_fig_subs_inds
from fig_heatmap import create_heatmap
from fig_subs_pos_neg import create_subs_pos_neg, create_slider
from fig_bubble import create_bubble_fig
from fig_table_views import create_table
from fig_image import make_image, prepare_data

channels, posts, reactions, subscribers, views = load_data()
processed_data = process_data(channels, posts, reactions, subscribers, views)

st.set_page_config(layout="wide", page_icon="🅢",)
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
        text-align: left;
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

    .custom-text { color: #666; 
                   font-size: 13px; 
                   } 
    .custom-number { color: brown; 
                     font-weight: bold; 
                     font-size: 17px; }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #ffb347;
        padding: 0rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .button-container {
        display: flex;
        justify-content: flex-start;
        gap: 0px;
        margin-bottom: 0px;
    }
    .stButton > button {
        background-color: #ffb347;
        border-color: #f5dfbf;
        color: #666;
        border: 2px solid #f5dfbf;
        border-radius: 20px;
        padding: 0px 8px;
        font-size: 8px;
        font-weight: 200;
        white-space: nowrap; 
        font-family: 'Roboto', sans-serif;
    }
    .stButton > button:hover {
        background-color: #f5dfbf;
        border-color: #f5dfbf;
        color: #666;
    }
    .stButton > button:active {
        background-color: #f5dfbf;
        border-color: #f5dfbf;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)




def main():
    
    posts = processed_data['posts']
    subs = processed_data['subs']
    gr_pvr = processed_data['gr_pvr']
    post_view = processed_data['post_view']
    
    col1, col2 = st.columns(2)
    with col1:
         # Заголовок
        st.markdown('<div class="title"><h1>Simulative</h1></div>', unsafe_allow_html=True)
        # Подзаголовок
        st.markdown('<div class="subheader"><h2>Дашборд по анализу Telegram-каналов</h2></div>', unsafe_allow_html=True)
        # Выбор канала
        channels_list = processed_data['posts']['channel_name'].unique()
        selected_channel = st.selectbox('Выберите канал:', channels_list)
    with col2:
        if selected_channel:
            df_words = prepare_data(posts, selected_channel)
            image = make_image(df_words)
            st.image(image, use_column_width=True)

    mean_subs_pos, mean_subs_neg, max_subs_pos, max_subs_neg = calculate_mean_max_subs(subs, selected_channel)
    mean_posts_day, mean_posts_week, mean_posts_month = calculate_mean_posts(posts, selected_channel)
    mean_views = calculate_mean_views(post_view, selected_channel)
    mean_reacts, mean_idx, react1, perc1, react2, perc2, react3, perc3 = calculate_mean_reacts(gr_pvr, selected_channel)
    
    fig_posts = create_fig_posts_inds(posts, selected_channel)
    fig_subs = create_fig_subs_inds(subs, selected_channel)

        # Инициализация состояния кнопок
    if 'button_state' not in st.session_state:
        st.session_state.button_state = "all (6м)"

    # Стили для чисел
    metric_styles = {
        "color": "#3366CC",
        "fontWeight": "bold",
        "fontSize": "20px"
    }
    
    st.markdown(
        """
        <style>
            .row {
                display: flex;
                margin-bottom: 40px;
            }
            .column {
                width: 22%;
                height: 100%;
                margin-right: 30px;
            }
            .last-column {
                margin-left: 30px;
            }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.write(f'<span class="custom-text"> 📈 Средний ежедневный прирост: </span><span class="custom-number">{mean_subs_pos}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 📉 Средний ежедневный отток: </span><span class="custom-number">{mean_subs_neg}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 🚀 Максимальный прирост: </span><span class="custom-number">{max_subs_pos}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 🆘 Максимальный отток: </span><span class="custom-number">{max_subs_neg}</span>', unsafe_allow_html=True)

    with col2:
        st.write(f'<span class="custom-text"> 📋 В среднем постов в день: </span><span class="custom-number">{mean_posts_day}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 📜 В среднем постов в неделю: </span><span class="custom-number">{mean_posts_week}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 🗂️ В среднем постов в месяц: </span><span class="custom-number">{mean_posts_month}</span>', unsafe_allow_html=True)

    with col3:
        st.write(f'<span class="custom-text"> 👀 В среднем просмотров: </span><span class="custom-number">{mean_views}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 🐾 В среднем реакций: </span><span class="custom-number">{mean_reacts}</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 💎 В среднем уровень активности: </span><span class="custom-number">{mean_idx}%</span>', unsafe_allow_html=True)

    with col4:
        st.write(f'<span class="custom-text"> 🥇 Доля реакции {react1}: </span><span class="custom-number">{perc1}%</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 🥈 Доля реакции {react2}: </span><span class="custom-number">{perc2}%</span>', unsafe_allow_html=True)
        st.write(f'<span class="custom-text"> 🥉 Доля реакции {react3}: </span><span class="custom-number">{perc3}%</span>', unsafe_allow_html=True)
        
    # Размещение графиков на одной строке
    col1, col2 = st.columns(2)
    with col1:    
        st.plotly_chart(fig_posts, use_container_width=True) 
        # Кастомный CSS для скрытия подписей под слайдером
        st.markdown(""" <style> .stSlider .st-cl::after { content: ""; } </style> """, unsafe_allow_html=True)
        slider = create_slider(subs, selected_channel)
        fig_subs_pos_neg = create_subs_pos_neg(subs, selected_channel, slider) #, slider
        st.plotly_chart(fig_subs_pos_neg, use_container_width=True)

        # Кнопки для выбора периода
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns([0.25, 0.15, 0.15, 0.15, 0.30])
        with button_col1:
            st.empty()          
        with button_col2:
            if st.button("3д", key="3db"):
                st.session_state.button_state = "3д"
        with button_col3:
            if st.button("1н", key="1wb"):
                st.session_state.button_state = "1н"
        with button_col4:
            if st.button("1м", key="1mb"):
                st.session_state.button_state = "1м"
        with button_col5:
            if st.button("all (6м)", key="6mb"):
                st.session_state.button_state = "all (6м)"
        st.markdown('</div>', unsafe_allow_html=True)

        # Фильтрация данных в зависимости от выбранной кнопки
        if st.session_state.button_state == "3д":
            filtered_bubble = gr_pvr[(gr_pvr.channel_name == selected_channel)&(pd.to_datetime(gr_pvr.post_datetime.str[:10])>=date_ago('days', 2))]  
        elif st.session_state.button_state == "1н":
            filtered_bubble = gr_pvr[(gr_pvr.channel_name == selected_channel)&(pd.to_datetime(gr_pvr.post_datetime.str[:10])>=date_ago('weeks', 1))]
        elif st.session_state.button_state == "1м":
            filtered_bubble = gr_pvr[(gr_pvr.channel_name == selected_channel)&(pd.to_datetime(gr_pvr.post_datetime.str[:10])>=date_ago('months', 1))]
        else:  # "all (6м)"
            filtered_bubble = gr_pvr[(gr_pvr.channel_name == selected_channel)&(pd.to_datetime(gr_pvr.post_datetime.str[:10])>=date_ago('months', 6))]
        
        fig_bubble = create_bubble_fig(filtered_bubble)
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    with col2:
        
        st.plotly_chart(fig_subs, use_container_width=True)
        
        # Кнопки для выбора периода
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        button_col1, button_col2, button_col3, button_col4, button_col5 = st.columns([0.25, 0.15, 0.15, 0.15, 0.30])
        with button_col1:
            st.empty()          
        with button_col2:
            if st.button("3д", key="3d"):
                st.session_state.button_state = "3д"
        with button_col3:
            if st.button("1н", key="1w"):
                st.session_state.button_state = "1н"
        with button_col4:
            if st.button("1м", key="1m"):
                st.session_state.button_state = "1м"
        with button_col5:
            if st.button("all (6м)", key="6m"):
                st.session_state.button_state = "all (6м)"
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


    # Добавление таблицы
        st.subheader("Динамика просмотров по дням")
        st.write(""" Эта таблица помогает определить оптимальное время для публикаций: если в первые сутки после публикации она собирает более 35% всех просмотров, это успешное время публикации; иначе стоит пересмотреть график размещения контента, чтобы новые публикации не затерялись среди конкурентов. Также можно обнаружить возможную мошенническую активность: например, если за одни сутки видео набирает 80% общего количества просмотров, следует проявить осторожность, проанализировать частоту подобных аномалий и сделать выводы (проценты приведены, как пример). """)
        st.slider("Количество дней для отображения", min_value=1, max_value=24, value=5, key="slider_days")
        days_to_show = st.session_state.slider_days
        columns_to_show = ["ID поста", "Дата публикации", "Текущие просмотры"] + [str(i)+" д" for i in range(1, days_to_show+1)]
        
        df = create_table(post_view, days_to_show, selected_channel)
        #def highlight_percentages(s):
        #    is_large = s > 80
        #    return ['background-color: lightgreen' if v else '' for v in is_large]
        
        #styled_df = df.style.apply(highlight_percentages, subset= [str(i)+" д" for i in range(1, days_to_show+1)])
        #st.dataframe(styled_df.to_html(), unsafe_allow_html=True)

        st.table(df[columns_to_show])

        #Поисковик
        st.subheader("Просмотр текста поста и даты по номеру ID:")
        # Здесь можно добавить фильтрацию и отображение конкретной строки из DataFrame
        post_id = st.text_input("Введите номер ID поста:", "")
        if post_id:
            try:
                #row = posts.query(f"'id' == '{post_id}'").iloc[0]
                row = posts[posts.id.astype(str) == post_id].iloc[0, :]
                st.write(f"ID: {row['id']}")
                st.write(f"Дата: {row['date']}")
                st.write(f"Время: {row['time']}")
                st.write(f"Текст поста: {row['text']}")
                #st.write(f"Дата поста: {row['date']}")
            except IndexError:
                st.error("Номер ID не найден.")



if __name__ == "__main__":
    main()


