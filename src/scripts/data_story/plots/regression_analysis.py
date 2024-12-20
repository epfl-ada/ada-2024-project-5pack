import pandas as pd
import plotly.express as px

from src.utils.strategies.comparison import perform_mixed_linear_regression


def generate_plot(data, output_dir):
	fig_fixed = plot_fixed_effects()
	fig_random = plot_random_effects()
	fig_fixed.write_html(output_dir / "fixed_effect.html", include_plotlyjs=True, full_html=True)
	fig_random.write_html(output_dir / "random_effect.html", include_plotlyjs=True, full_html=True)


def plot_fixed_effects():
	result = perform_mixed_linear_regression()

	# Extract fixed effects parameters excluding the Intercept
	fe_params = result.fe_params.drop("Intercept")

	# Create a DataFrame for plotting
	fe_params_df = pd.DataFrame(fe_params, columns=["Coefficient"]).reset_index()
	fe_params_df.columns = ["Feature", "Coefficient"]

	# Plot using plotly with horizontal bars
	fig = px.bar(fe_params_df, x="Coefficient", y="Feature", orientation="h", title="Fixed Effects Coefficients")
	return fig


def plot_random_effects():
	result = perform_mixed_linear_regression()
	random_effects = result.random_effects

	random_effects_df = pd.DataFrame.from_dict(random_effects, orient="index", columns=["Group"])

	fig = px.histogram(random_effects_df, x="Group", nbins=50, title="Distribution of Random Effects")

	top_5 = random_effects_df.nlargest(5, "Group")
	bottom_5 = random_effects_df.nsmallest(5, "Group")

	annotations = []
	for i, (idx, row) in enumerate(top_5.iterrows()):
		annotations.append(
			dict(x=row["Group"], y=0, xref="x", yref="y", text=f"{idx}", showarrow=True, arrowhead=2, ax=0, ay=-i * 30 - 20)
		)

	for i, (idx, row) in enumerate(bottom_5.iterrows()):
		annotations.append(
			dict(x=row["Group"], y=0, xref="x", yref="y", text=f"{idx}", showarrow=True, arrowhead=2, ax=0, ay=-i * 30 - 20)
		)

	fig.update_layout(annotations=annotations)
	return fig
