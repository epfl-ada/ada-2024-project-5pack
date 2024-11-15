"""
Main analysis script for Wikispeedia dataset
"""

import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.utils.semantic_analyzer import SemanticAnalyzer
from src.utils import logger
from src.utils.data_utils import load_graph_data
from src.utils.network_analyzer import NetworkAnalyzer
from src.utils.path_analyzer import PathAnalyzer
from src.utils.statistical_tests import StatisticalAnalyzer
from src.utils.visualizations import WikispeediaVisualizer

RESULTS_DIR = Path("./data/generated/plaintext_analysis")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Used for custom JSON serialization
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        return super(NpEncoder, self).default(obj)

def setup_results_directory():
    """Create timestamped results directory."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = RESULTS_DIR / f'analysis_{timestamp}'
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir

def analyze_network(graph_data, results_dir):
    """Perform network analysis."""
    logger.info("Performing network analysis...")
    network_analyzer = NetworkAnalyzer()
    
    # Use the pre-built graph from graph_data
    network_analyzer.graph = graph_data['graph']
    logger.info(f"Using pre-built graph with {network_analyzer.graph.number_of_nodes()} nodes and "
               f"{network_analyzer.graph.number_of_edges()} edges")
    
    # Compute network metrics
    network_metrics = network_analyzer.compute_network_metrics()
    
    # Identify hub articles
    network_analyzer.identify_hubs(top_n=50)
    network_analyzer.compute_centrality_metrics()
    
    # Save network metrics
    with open(results_dir / 'network_metrics.json', 'w') as f:
        json.dump(network_metrics, f, indent=4, default=str)
    
    return network_analyzer

def analyze_paths(graph_data, network_analyzer, results_dir):
    """Perform path analysis."""
    logger.info("Performing path analysis...")
    
    # Initialize analyzers
    semantic_analyzer = SemanticAnalyzer()
    path_analyzer = PathAnalyzer(
        semantic_analyzer=semantic_analyzer,
        network_analyzer=network_analyzer
    )
    
    # Process articles for semantic analysis
    articles_df = graph_data['articles'].copy()
    semantic_analyzer.process_articles(articles_df)
    
    # Analyze paths
    paths_df = path_analyzer.analyze_paths(
        paths_finished=graph_data['paths_finished'],
        paths_unfinished=graph_data['paths_unfinished']
    )
    
    # Compute statistics
    path_stats = path_analyzer.compute_path_statistics(paths_df)
    time_patterns = path_analyzer.analyze_time_patterns(paths_df)
    
    # Save results
    paths_df.to_csv(results_dir / 'analyzed_paths.csv', index=False)
    with open(results_dir / 'path_statistics.json', 'w') as f:
        json.dump(path_stats, f, indent=4, default=str)
    
    return paths_df, path_stats, time_patterns


def perform_statistical_analysis(paths_df, results_dir):
    """Perform comprehensive statistical analysis."""
    logger.info("Performing statistical analysis...")
    stat_analyzer = StatisticalAnalyzer()
    
    # Test strategy effectiveness
    strategy_results = stat_analyzer.test_strategy_effectiveness(paths_df)
    
    # Create semantic distances dictionary from semantic coherence
    if 'semantic_coherence' in paths_df.columns:
        semantic_dict = {}
        for _, row in paths_df.iterrows():
            if isinstance(row['path'], list) and len(row['path']) >= 2:
                start, end = row['path'][0], row['path'][-1]
                semantic_dict[(start, end)] = row['semantic_coherence']
        
        # Test semantic proximity hypothesis
        semantic_results = stat_analyzer.test_semantic_proximity_hypothesis(
            paths_df,
            semantic_dict
        )
    else:
        semantic_results = {
            'test_name': 'Semantic Proximity Test',
            'statistic': None,
            'p_value': None,
            'effect_size': None,
            'successful_mean': None,
            'failed_mean': None,
            'sample_size': 0
        }
    
    # Fit and evaluate prediction model
    model_results = stat_analyzer.fit_logistic_regression(paths_df)
    
    # Save results
    with open(results_dir / 'statistical_results.json', 'w') as f:
        results = {
            'strategy_analysis': {
                'test_name': strategy_results['test_name'],
                'chi2': float(strategy_results['chi2']),
                'p_value': float(strategy_results['p_value']),
                'effect_size': float(strategy_results['effect_size']),
                'success_rates': strategy_results['success_rates']
            },
            'semantic_analysis': {
                'test_name': semantic_results['test_name'],
                'p_value': semantic_results.get('p_value'),
                'effect_size': semantic_results.get('effect_size'),
                'sample_size': semantic_results.get('sample_size')
            },
            'model_performance': {
                'roc_auc': float(model_results['roc_auc']),
                'cv_scores': {
                    'mean': float(model_results['cv_scores']['mean']),
                    'std': float(model_results['cv_scores']['std'])
                },
                'feature_importance': model_results['feature_importance']  # Already in the correct format
            }
        }
        
        json.dump(results, f, indent=4, cls=NpEncoder)
    
    return strategy_results, model_results

def create_visualizations(
    paths_df, network_analyzer, model_results, 
    path_stats, time_patterns, results_dir
):
    """Create and save visualizations."""
    logger.info("Creating visualizations...")
    visualizer = WikispeediaVisualizer()
    
    try:
        # Create figures
        figs = {}
        
        # Navigation patterns - combine stats into a single dict
        nav_stats = {
            'path_stats': path_stats,
            'time_patterns': time_patterns
        }
        figs['navigation_patterns'] = visualizer.plot_navigation_patterns(
            paths_df, nav_stats
        )
        
        # Network structure
        figs['network_structure'] = visualizer.plot_network_structure(
            network_analyzer.graph,
            network_analyzer.centrality_metrics
        )
        
        # Model performance
        figs['model_performance'] = visualizer.plot_model_performance(model_results)
        
        # Temporal patterns
        figs['temporal_patterns'] = visualizer.plot_temporal_patterns(time_patterns)
        
        # Save figures
        for name, fig in figs.items():
            if fig is not None:  # Only save if figure was created
                filepath = results_dir / f'{name}.png'
                fig.savefig(filepath, dpi=300, bbox_inches='tight')
                plt.close(fig)
                logger.info(f"Saved {name} visualization to {filepath}")
    
    except Exception as e:
        logger.error(f"Error creating visualizations: {str(e)}")
        # Continue with the analysis even if visualizations fail
        return

def generate_report(
    network_metrics, path_stats, strategy_results, 
    model_results, time_patterns, results_dir
):
    """Generate analysis report."""
    logger.info("Generating analysis report...")
    
    # Convert feature importance list to dict but need to handle different cases
    feature_importance = model_results.get('feature_importance', [])
    if isinstance(feature_importance, list):
        feature_importance_dict = {
            f"feature_{i}": feat for i, feat in enumerate(feature_importance)
        }
    elif hasattr(feature_importance, 'to_dict'):
        feature_importance_dict = feature_importance.to_dict()
    else:
        feature_importance_dict = feature_importance

    report = {
        'summary': {
            'total_paths_analyzed': path_stats['basic_stats']['total_paths'],
            'success_rate': path_stats['basic_stats']['success_rate'],
            'network_size': network_metrics['basic_metrics']['nodes'],
            'model_performance': model_results['cv_scores']['mean']
        },
        'network_analysis': network_metrics,
        'path_analysis': path_stats,
        'navigation_strategies': strategy_results,
        'temporal_patterns': time_patterns,
        'model_evaluation': {
            'performance': model_results['classification_report'],
            'feature_importance': feature_importance_dict
        }
    }
    
    # Ensure all values are JSON serializable to dump to file
    def convert_to_serializable(obj):
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(v) for v in obj]
        return obj

    # Convert the report to serializable format
    serializable_report = convert_to_serializable(report)
    
	# Save
    with open(results_dir / 'analysis_report.json', 'w') as f:
        json.dump(serializable_report, f, indent=4, default=str)

def main():
    """Run complete Wikispeedia data analysis pipeline."""
    # Setup
    results_dir = setup_results_directory()
    logger.info(f"Analysis results will be saved to: {results_dir}")
    
    try:
        # Load data using the existing utility
        logger.info("Loading data...")
        graph_data = load_graph_data()
        
        # Perform analyses
        network_analyzer = analyze_network(graph_data, results_dir)
        paths_df, path_stats, time_patterns = analyze_paths(
            graph_data, network_analyzer, results_dir
        )
        strategy_results, model_results = perform_statistical_analysis(
            paths_df, results_dir
        )
        
        # Create visualizations
        create_visualizations(
            paths_df, network_analyzer, model_results,
            path_stats, time_patterns, results_dir
        )
        
        # Generate final report
        generate_report(
            network_analyzer.compute_network_metrics(),
            path_stats,
            strategy_results,
            model_results,
            time_patterns,
            results_dir
        )
        
        logger.info(f"Analysis complete. Results saved to {results_dir}")
        return results_dir
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise

if __name__ == "__main__":
    results_dir = main()