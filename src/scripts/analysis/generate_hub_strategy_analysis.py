from pathlib import Path

from src.utils.strategies.hub_focused_strategy import find_optimal_parameters

RESULTS_DIR = Path("./data/generated/strategies/")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
	results_df, optimal_params = find_optimal_parameters()

	print("\nHub Strategy Analysis Results:")
	print(f"Optimal number of hubs: {optimal_params['n_hubs']}")
	print(f"Optimal usage threshold: {optimal_params['threshold']:.2f}")
	print(f"Success rate at optimal parameters: {optimal_params['success_rate']:.2%}")
	print(
		f"Percentage of paths using strategy: {optimal_params['paths_percentage']:.2%}",
	)

	# Save detailed results
	results_df.to_csv(RESULTS_DIR / "hub_strategy_analysis.csv", index=False)
