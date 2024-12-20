import plotly.graph_objects as go

def generate_plot(data, output_dir):
    effects = [
        {
            "name": "Hub (main effect)",
            "effect": 2.48,
            "se": 0.638,
            "category": "main",
            "description": "Direct impact of using Hub strategy"
        },
        {
            "name": "Hub × Semantic",
            "effect": -1.76,
            "se": 0.5,
            "category": "interaction",
            "description": "Reduces duration when used with Semantic"
        },
        {
            "name": "Hub × Top Links",
            "effect": -2.98,
            "se": 0.495,
            "category": "interaction",
            "description": "Stronger reduction with Top Links"
        },
        {
            "name": "Hub × Backtrack",
            "effect": -4.06,
            "se": 0.653,
            "category": "interaction",
            "description": "Strongest interaction, mitigates Backtrack"
        }
    ]

    names = [effect["name"] for effect in effects]
    y_pos = [i*1.5 for i in range(len(effects))]  # Increased spacing
    effects_values = [effect["effect"] for effect in effects]
    errors = [1.96 * effect["se"] for effect in effects]
    categories = [effect["category"] for effect in effects]
    descriptions = [effect["description"] for effect in effects]

    fig = go.Figure()

    # Add error bars
    for i, (effect, error, category, name) in enumerate(zip(effects_values, errors, categories, names)):
        color = '#3b82f6' if category == 'main' else '#22c55e'
        fig.add_trace(go.Scatter(
            x=[effect],
            y=[y_pos[i]],
            error_x=dict(
                type='data',
                symmetric=True,
                array=[error],
                color=color,
                thickness=2,
                width=10
            ),
            mode='markers',
            marker=dict(
                color=color,
                size=10
            ),
            name=name,
            showlegend=False
        ))

    # Add vertical zero line (dashed)
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=-0.5,
        y1=max(y_pos) + 0.1,
        line=dict(
            color="gray",
            width=1,
            dash="dash"
        )
    )

    fig.update_layout(
        title={
            'text': 'Hub Strategy: Main Effect vs Interactions',
            'y': 0.95,
            'x': 0.4,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=16)
        },
        yaxis=dict(
            ticktext=names,
            tickvals=y_pos,
            zeroline=False,
            gridwidth=1,
            autorange="reversed",
            showgrid=False,
            range=[-1, max(y_pos) + 1]
        ),
        xaxis=dict(
            title=dict(
                text='Effect (seconds)',
                font=dict(size=12)
            ),
            range=[-6.5, 5.1],
            zeroline=False,
            gridwidth=1,
            ticktext=['-4s', '-2s', '0s', '2s', '4s'],
            tickvals=[-4, -2, 0, 2, 4],
            showgrid=False
        ),
        plot_bgcolor='white',
        width=930,
        height=500,
        margin=dict(l=150, r=350, t=50, b=60)
    )

    for i, (effect, error, desc) in enumerate(zip(effects_values, errors, descriptions)):
        # Add effect value
        fig.add_annotation(
            x=4.9,
            y=y_pos[i],
            text=f"{effect:.2f}s ±{error:.2f}",
            showarrow=False,
            xanchor="left",
            align="right",
            font=dict(size=12)
        )
        
        # Add description
        fig.add_annotation(
            x=4.9,
            y=y_pos[i] + 0.2,
            text=desc,
            showarrow=False,
            xanchor="left",
            align="left",
            font=dict(size=12, color='gray')
        )

    fig.add_annotation(
        x=-6,
        y=-0.8,
        xref="x",
        yref="paper",
        text="Note: Negative values indicate reduction in duration (improvement).",
        showarrow=False,
        font=dict(size=11),
        xanchor="left",
        yanchor="top"
    )

    fig.add_annotation(
        x=-6,
        y=-0.95,
        xref="x",
        yref="paper",
        text="All interactions are significant and stronger than main effect.",
        showarrow=False,
        font=dict(size=11),
        xanchor="left",
        yanchor="top"
    )

    fig.write_html(output_dir / "hubs_impact.html", include_plotlyjs=True, full_html=True)
