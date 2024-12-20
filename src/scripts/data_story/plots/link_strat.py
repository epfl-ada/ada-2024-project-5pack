import pandas as pd
import numpy as np
from src.utils.link_strategy import get_click_positions, get_probability_link


import plotly.express as px
import numpy as np
from src.utils.link_strategy import get_click_positions, build_link_order
from src.utils.strategies.comparison import build_comparison_df
from src.utils.metrics import average_on_paths, pagerank

def generate_plot(data, output_dir):
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt

	from src.utils.data_utils import load_graph_data

	graph_data = load_graph_data()

	all_links_dict = build_link_order()
	fig = pie(graph_data, all_links_dict)
	fig.write_html(output_dir / "pie_top_clicks.html", include_plotlyjs=True, full_html=True)

	finished, unfinished = build_comparison_df(graph_data, all_links_dict)
	

	barplot_success, barplot_times = comparison_performance(graph_data, all_links_dict, finished, unfinished)
	barplot_success.write_html(output_dir / "barplot_success.html", include_plotlyjs=True, full_html=True)
	barplot_times.write_html(output_dir / "barplot_times.html", include_plotlyjs=True, full_html=True)


	plot_gen = generality_behavior(graph_data)
	plot_gen.write_html(output_dir / "plot_gen.html", include_plotlyjs=True, full_html=True)


	link_barplot = times_comparison(finished)
	link_barplot.write_html(output_dir / "link_barplot.html", include_plotlyjs=True, full_html=True)



def pie(graph_data, all_links_dict) -> px:
	paths_finished = graph_data['paths_finished']
	click_positions_fin = get_click_positions(paths_finished, all_links_dict)

	top_links = [pos for pos in click_positions_fin if pos <= 0.2]
	otherlinks = [pos for pos in click_positions_fin if pos > 0.2]

	labels = ['Top 20%', 'Bottom 80%']
	sizes = [len(top_links), len(otherlinks)]

	fig = px.pie(
		names=labels,
		values=sizes,
		title="Proportion of clicks on top 20% links vs bottom 80%",
	)

	fig.update_traces(texttemplate='%{percent:.1%}',textposition='inside')
	return fig

def generality_behavior(graph_data):

	scores, percent = average_on_paths(10, graph_data['paths_finished'], pagerank(graph_data['graph']))

	fig = px.line(x=percent, y=scores, labels={'x': 'Percentage of path','y': 'Generality Score (higher is more general)'},
		title='Average generality behavior (taken accross all finished paths)')

	return fig


def times_comparison(finished):
	bins = [0, 0.6, 0.8, 1.0]
	labels = ['0-60%', '61-80%', '81-100%']

	finished['bin'] = pd.cut(finished['link_percentage'], bins=bins, labels=labels, include_lowest=True)

	avg_time_finished = finished.groupby('bin').agg(
		avg_completion_time=('time', 'mean'),
		number=('time', 'count')
	).reset_index()


	global_avg_time_finished = finished['time'].mean()

	fig = px.bar(avg_time_finished, x='bin', y='avg_completion_time',
				title='Average time by top links usage',
				labels={'bin': 'Percentage of clicks on top links', 'avg_completion_time': 'Average time (seconds)'},
				color='bin',
				hover_data={
			'bin': False,  
			'avg_completion_time': ':.2f',  
			'number': True  
		})

	# Horizontal line for the global mean
	fig.add_shape(type="line",
				x0=-0.5, x1=2.5, y0=global_avg_time_finished, y1=global_avg_time_finished,
				line=dict(color="Red", dash="dash"))

	fig.add_annotation(x=2, y=global_avg_time_finished,
					text=f"Average game time : {global_avg_time_finished:.2f} seconds",
					showarrow=False,
					yshift=10)
	return fig



def comparison_performance(graph_data, all_links_dict, finished, unfinished):
	all_paths = pd.concat([finished, unfinished])

	#success
	global_success_rate = all_paths['finished'].mean()
	success_link = all_paths[all_paths['top_link_usage']]['finished'].mean()
	success_semantic = all_paths[all_paths['semantic']]['finished'].mean()
	success_maxgen = all_paths[all_paths['max_generality']]['finished'].mean()

	#times (finished)
	global_avg_time = finished['time'].mean()
	time_link = finished[finished['top_link_usage']]['time'].mean()
	time_semantic = finished[finished['semantic']]['time'].mean()
	time_maxgen = finished[finished['max_generality']]['time'].mean()

	categories = ['Global', 'Link>0.8', 'Semantic>0.8', 'Visit top 200 articles']

	success_rates = [global_success_rate, success_link, success_semantic, success_maxgen]
	success_data = pd.DataFrame({
		'Category': categories,
		'Success Rate': success_rates
	})

	barplot_success = px.bar(
		success_data,
		x='Category',
		y='Success Rate',
		title='Success Rates Comparison',
		labels={'Success Rate': 'Success Rate'},
		color='Category',
		color_discrete_sequence=px.colors.sequential.Plasma
	)


	avg_times = [global_avg_time, time_link, time_semantic, time_maxgen]
	times_data = pd.DataFrame({
		'Category': categories,
		'Average time (seconds)': avg_times
	})

	barplot_times = px.bar(
		times_data,
		x='Category',
		y='Average time (seconds)',
		title='Average time (Finished Only)',
		labels={'Average time (seconds)': 'Average time (seconds)'},
		color='Category',
		color_discrete_sequence=px.colors.sequential.Viridis
	)

	return barplot_success, barplot_times


