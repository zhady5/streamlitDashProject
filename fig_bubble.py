


def create_bubble_fig(filtered_df):
#table
        gr_pvr_sum = filtered_df.drop(['reaction_type', 'react_cnt'], axis=1).drop_duplicates()
    
        if gr_pvr_sum.shape[0] == 0:
            return {}
        
        # Создаем градиент 
        colors = cl.scales['9']['seq']['OrRd'][::-1] 
        
    # Предположим, что у тебя уже есть DataFrame под названием gr_pvr_sum
        fig = go.Figure()
        
        # Добавление точек на график
        fig.add_trace(go.Scatter(
            x=gr_pvr_sum['current_views'],
            y=gr_pvr_sum['idx_active'],
            mode='markers',
            marker=dict(
                size=gr_pvr_sum['react_cnt_sum'],
                color=gr_pvr_sum['current_views'],
                colorscale=colors,
                showscale=False,  # Скрывает colorbar
                sizemode='area',
                sizeref=2. * max(0, max(gr_pvr_sum['react_cnt_sum'])) / (18.**2),
                sizemin=4
            ),
            text=gr_pvr_sum[['post_id']],  # Показывает post_id и дату при наведении
            hoverinfo='text+x+y+z',  # Настройка информации во всплывающей подсказке
            hovertemplate=
                '<b>ID Поста:</b> %{text}<br>' +
                '<b>Текущие Просмотры:</b> %{x}<br>' +
                '<b>Количество реакций:</b> %{marker.size}<br>' +  # Добавлен размер пузыря
                '<b>Активность:</b> %{y} %<extra></extra>'
        ))
        
        # Логарифмическая ось X
        fig.update_xaxes(type="log")
    
    
        # Скрыть colorbar
        fig.update_layout(coloraxis_showscale=False)
    
        fig.update_layout(    
            yaxis_title="Индекс активности, %",
            xaxis_title="Текущее количество просмотров",         
            xaxis=dict(
                showgrid=False,
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                #dtick=10,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)',
            ),
            margin=dict(l=40, r=60, t=10, b=10),
            showlegend=False,
            paper_bgcolor='#ffb347',
            plot_bgcolor='#ffb347',
            hovermode='closest',
        )
        return fig    
