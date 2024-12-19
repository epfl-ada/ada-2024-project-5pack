from src.utils.strategies.semantic_strategy import get_semantic_similarity
import plotly.figure_factory as ff
import numpy as np

def generate_plot(data, output_dir):
    fig = similarity_matrix_figure()
    fig.write_html(output_dir / "similarity_matrix.html", include_plotlyjs=True, full_html=True)

def similarity_matrix_figure() -> ff:
    articles = ['Bee', 'Tree', 'Computer', 'Linux', 'Flower']

    # Compute the confusion matrix
    confusion_matrix = np.zeros((len(articles), len(articles)))
    for i, article1 in enumerate(articles):
        for j, article2 in enumerate(articles):
            confusion_matrix[i, j] = get_semantic_similarity(article1, article2)


    # TODO Fred: Fix color scale
    fig = ff.create_annotated_heatmap(
        z=np.round(confusion_matrix, 3),
        x=articles,
        y=articles,
        colorscale='Viridis'
    )

    fig.update_layout(
        title='Semantic Similarity Confusion Matrix',
        xaxis_title='Articles',
        yaxis_title='Articles',
        autosize=False,
        width=500,
        height=500
    )

    # Add color bar
    fig['data'][0]['colorbar'] = dict(
        title='Cosine Similarity',
        titleside='right',
        tickvals=[0, 0.25, 0.5, 0.75, 1],
        ticktext=['0', '0.25', '0.5', '0.75', '1']
    )
    fig['data'][0]['showscale'] = True

    return fig
