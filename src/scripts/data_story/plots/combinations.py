import math
import plotly.graph_objects as go

def generate_plot(data, output_dir):
    strategies = ['Backtrack only', 'No strategies', 'All strategies', 'Semantic only', 'Semantic + Top Links']
    durations = [193.5, 156.1, 156.0, 135.6, 127.4]
    colors = ['#9E9E9E', '#2196F3', '#2196F3', '#9E9E9E', '#4CAF50']
    variances = [
        (1.098)**2+(0.625)**2,
        (1.098)**2,
        (1.098)**2+(0.625)**2+(0.528)**2+(0.549)**2+(0.639)**2,
        (1.098)**2+(0.528)**2,
        (1.098)**2+(0.528)**2+(0.549)**2
    ]
    error_bars = [1.96 * math.sqrt(var) for var in variances]

    figure = go.Figure()

    for i in range(len(strategies)):
        figure.add_trace(go.Scatter(
            x=[durations[i]],
            y=[strategies[i]],
            mode='markers',
            error_x=dict(
                type='data',
                array=[error_bars[i]],
                visible=True,
                color=colors[i],
                thickness=1.5,
                width=8
            ),
            marker=dict(
                color=colors[i],
                size=8,
                symbol='circle'
            )
        ))

    figure.update_layout(
        title=dict(
            text='Strategy Combinations Impact on Duration',
            x=0.01,
            font=dict(size=24, color='rgb(44, 62, 80)')
        ),
        plot_bgcolor='rgba(240, 244, 250, 0.8)',
        paper_bgcolor='white',
        xaxis=dict(
            title='Duration',
            title_font=dict(size=16, color='rgb(44, 62, 80)'),
            range=[110, 210],
            ticksuffix='s',
            tickmode='array',
            tickvals=[120, 140, 160, 180, 200],
            ticktext=['120s', '140s', '160s', '180s', '200s'],
            gridcolor='white',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            automargin=True,
            gridcolor='white',
            showgrid=True,
            zeroline=False,
            title='',
            tickfont=dict(size=12)
        ),
        width=930,
        height=400,
        margin=dict(l=150, r=30, t=50, b=50),
        showlegend=False
    )

    figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white')
    figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white')

    figure.write_html(output_dir / "strategies_combinations.html", include_plotlyjs=True, full_html=True)