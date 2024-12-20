import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
import numpy as np

def compute_backtrack_statistics(data: dict) -> dict:
    """Compute comprehensive backtracking statistics."""
    finished_paths = data["paths_finished"]
    unfinished_paths = data["paths_unfinished"]
    
    # Calculate statistics for both path types
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
   
   # Plot histograms and mean lines 
   for path_type in ["Finished", "Unfinished"]:
       df = stats[path_type]
       mean_ratio = df["backtrack_ratio"].mean()
       means[path_type] = mean_ratio
       
       # Add histogram
       fig.add_trace(go.Histogram(
           x=df["backtrack_ratio"],
           name=f"{path_type} Paths",
           nbinsx=50,
           marker_color=colors[path_type],
           opacity=0.7,
           autobinx=False,
           xbins=dict(start=0, end=0.5, size=0.01)
       ))
       
       # Add mean line
       fig.add_vline(
           x=mean_ratio,
           line_dash="dash",
           line_color=colors[path_type]
       )
   
   # Calculate statistics for annotations
   total_paths = len(data['paths_finished']) + len(data['paths_unfinished'])
   finished_pct = len(data['paths_finished'])/total_paths * 100
   
   # Create x-axis ticks (regular intervals)
   tick_vals = list(np.arange(0, 0.6, 0.1))
   tick_text = [f"{x:.1f}" for x in tick_vals]
   
   fig.update_layout(
       title="Distribution of Backtrack Ratios<br><sup>Comparing finished vs unfinished paths</sup>",
       xaxis_title="Backtrack Ratio (BR = backtrack steps / total steps)",
       yaxis_title="Number of Paths",
       template="plotly_white",
       barmode="overlay",
       plot_bgcolor='white',
       
       # Axis settings
       xaxis=dict(
           range=[0, 0.5],
           tickvals=tick_vals,
           ticktext=tick_text,
           showgrid=True,
           gridwidth=1,
           gridcolor='lightgray'
       ),
       yaxis=dict(
           showgrid=True,
           gridwidth=1,
           gridcolor='lightgray'
       ),
       
       # Legend
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
       
       # Annotations
       annotations=[
           # Stats box
           dict(
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
           ),
           # Mean values under their dashed lines
           dict(
               x=means["Finished"],
               y=0,
               yref="paper",
               text=f"{means['Finished']:.3f}",
               showarrow=False,
               yshift=-15,
               font=dict(color=colors["Finished"])
           ),
           dict(
               x=means["Unfinished"],
               y=0,
               yref="paper",
               text=f"{means['Unfinished']:.3f}",
               showarrow=False,
               yshift=-25,
               font=dict(color=colors["Unfinished"])
           )
       ],
       margin=dict(r=300, t=100, b=100, l=100)
   )
   
   return fig

def generate_plot(data: dict, output_dir: Path) -> None:
    """Generate and save the plot."""
    fig = create_backtrack_analysis_plot(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / "backtrack_analysis.html", include_plotlyjs=True, full_html=True)