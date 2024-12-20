import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
import numpy as np

def compute_backtrack_statistics(data: dict) -> dict:
    """Compute comprehensive backtracking statistics."""
    finished_paths = data["paths_finished"]
    unfinished_paths = data["paths_unfinished"]
    
    stats = {}
    for path_type, paths_df in [("Finished", finished_paths), ("Unfinished", unfinished_paths)]:
        paths_stats = []
        for _, row in paths_df.iterrows():
            path = row["path"]
            backtrack_count = sum(1 for step in path if step == "<")
            paths_stats.append({
                "path_length": len(path),
                "backtrack_count": backtrack_count,
                "backtrack_ratio": backtrack_count / len(path) if path else 0,
                "duration": row["duration_in_seconds"]
            })
        stats[path_type] = pd.DataFrame(paths_stats)
    
    return stats

def create_backtrack_analysis_plot(data: dict) -> go.Figure:
    """Create visualization of backtracking patterns between finished and unfinished paths."""
    stats = compute_backtrack_statistics(data)
    
    fig = go.Figure()
    colors = {"Finished": "#2ecc71", "Unfinished": "#e74c3c"}
    means = {}
    
    for path_type in ["Finished", "Unfinished"]:
        df = stats[path_type]
        mean_ratio = df["backtrack_ratio"].mean()
        means[path_type] = mean_ratio
        
        # Add histogram with offsets for side-by-side bins
        fig.add_trace(go.Histogram(
            x=df["backtrack_ratio"],
            name=f"{path_type} Paths",
            nbinsx=50,
            marker_color=colors[path_type],
            opacity=0.9,
            autobinx=False,
            xbins=dict(start=0, end=0.5, size=0.01),
            offsetgroup=path_type,  # Group bars for side-by-side display
        ))
        
        # Add dashed line for mean
        fig.add_shape(
            type="line",
            x0=mean_ratio,
            x1=mean_ratio,
            y0=0,  # Start at the bottom of the y-axis
            y1=1,  # End at the top of the plot area (normalized units)
            line=dict(color=colors[path_type], dash="dash"),
            xref="x",
            yref="paper"
        )
        
        # Add transparent scatter trace for legend entry
        fig.add_trace(go.Scatter(
            x=[None],  # Invisible point
            y=[None],  # Invisible point
            mode="lines",
            line=dict(color=colors[path_type], dash="dash"),
            name=f"Mean BR ({path_type})"
        ))
    
    # Add annotations for mean ratios
    fig.add_annotation(
        x=means["Finished"],
        y=1,  # Place the annotation at the top
        yref="paper",
        text=f"{means['Finished']:.3f}",
        showarrow=False,
        font=dict(color=colors["Finished"]),
        align="center",
        yshift=10  # Slightly above the default position
    )
    fig.add_annotation(
        x=means["Unfinished"],
        y=1,  # Place the annotation at the top
        yref="paper",
        text=f"{means['Unfinished']:.3f}",
        showarrow=False,
        font=dict(color=colors["Unfinished"]),
        align="center",
        yshift=25  # Higher than the "Finished" annotation to avoid overlap
    )
    
    total_paths = len(data['paths_finished']) + len(data['paths_unfinished'])
    finished_pct = len(data['paths_finished']) / total_paths * 100
    
    tick_vals = list(np.arange(0, 0.6, 0.1))
    tick_text = [f"{x:.1f}" for x in tick_vals]
    
    fig.update_layout(
        title="Distribution of Backtrack Ratios<br><sup>Comparing finished vs unfinished paths</sup>",
        xaxis=dict(
            range=[0, 0.5],
            tickvals=tick_vals,
            ticktext=tick_text,
            title="Backtrack Ratio",
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            title="Number of Paths (Log Scale)",
            type="log"
        ),
        template="plotly_white",
        barmode="group",  # Group bars for side-by-side display
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.15,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),
        margin=dict(r=300, t=100, b=100, l=100)
    )
    
    # Add the stats that we got from the compute_backtrack_statistics
    fig.add_annotation(
        x=1.02,
        y=0.99,
        xref="paper",
        yref="paper",
        text=(
            f"Total Paths: {total_paths:,}<br>"
            f"Finished: {len(data['paths_finished']):,} ({finished_pct:.1f}%)<br>"
            f"Unfinished: {len(data['paths_unfinished']):,} ({100-finished_pct:.1f}%)"
        ),
        showarrow=False,
        align="left",
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    return fig

def generate_plot(data: dict, output_dir: Path) -> None:
    """Generate and save the plot."""
    fig = create_backtrack_analysis_plot(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / "backtrack_analysis.html", include_plotlyjs=True, full_html=True)