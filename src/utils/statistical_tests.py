"""
Statistical Tests Module
----------------------
Performs statistical analysis on Wikispeedia navigation data including:
- Hypothesis testing
- Logistic regression modeling
- Feature significance analysis
- Path characteristics analysis
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

from src.utils import AnalysisError, logger

ANALYSIS_PARAMS = {"test_size": 0.2, "random_state": 42, "cv_folds": 5, "significance_level": 0.05}

# Feature definitions
PATH_FEATURES = [
	"path_length",
	"backtrack_count",
	"unique_articles",
	"path_efficiency",
	"hub_usage_ratio",
	"avg_time_per_click",
	"semantic_coherence",
]

class StatisticalAnalyzer:
    def __init__(self):
        """Initialize StatisticalAnalyzer"""
        self.scaler = StandardScaler()
        self.model = None
        self.feature_stats = None
        
    def test_semantic_proximity_hypothesis(self, paths_df, semantic_distances):
        """Test hypothesis: Semantic proximity between start/end affects success"""
        try:
            logger.info("Testing semantic proximity hypothesis...")
            
            def get_semantic_distance(row):
                if not isinstance(row['path'], list) or len(row['path']) < 2:
                    return None
                start = row['path'][0]
                end = row['path'][-1]
                return semantic_distances.get((start, end))
            
            # Calculate semantic distances
            paths_df['semantic_distance'] = paths_df.apply(get_semantic_distance, axis=1)
            
            # Remove paths with missing distances
            valid_paths = paths_df.dropna(subset=['semantic_distance'])
            
            if len(valid_paths) < 2:
                logger.warning("Not enough valid paths for semantic analysis")
                return {
                    'test_name': 'Semantic Proximity Test',
                    'statistic': None,
                    'p_value': None,
                    'effect_size': None,
                    'sample_size': 0
                }
            
            # Compare distances
            successful = valid_paths[valid_paths['success']]['semantic_distance']
            failed = valid_paths[~valid_paths['success']]['semantic_distance']
            
            # Perform t-test
            t_stat, p_value = ttest_ind(successful, failed)
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(
                (successful.var() * (len(successful) - 1) + 
                failed.var() * (len(failed) - 1)) / 
                (len(successful) + len(failed) - 2)
            )
            cohens_d = (successful.mean() - failed.mean()) / pooled_std
            
            results = {
                'test_name': 'Semantic Proximity Test',
                'statistic': t_stat,
                'p_value': p_value,
                'effect_size': cohens_d,
                'successful_mean': successful.mean(),
                'failed_mean': failed.mean(),
                'sample_size': len(valid_paths)
            }
            
            logger.info(f"Semantic proximity test completed: p-value = {p_value:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic proximity test: {str(e)}")
            raise AnalysisError(f"Semantic proximity analysis failed: {str(e)}")
    
    def fit_logistic_regression(self, paths_df):
        """Fit logistic regression model to predict navigation success"""
        try:
            logger.info("Fitting logistic regression model...")
            
            # Check if we have all required features
            missing_features = [f for f in PATH_FEATURES if f not in paths_df.columns]
            if missing_features:
                logger.warning(f"Missing features: {missing_features}")
                available_features = [f for f in PATH_FEATURES if f in paths_df.columns]
                logger.info(f"Using available features: {available_features}")
                X = paths_df[available_features]
            else:
                X = paths_df[PATH_FEATURES]
            
            y = paths_df['success']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=ANALYSIS_PARAMS['test_size'],
                random_state=ANALYSIS_PARAMS['random_state']
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Fit model
            self.model = LogisticRegression(random_state=ANALYSIS_PARAMS['random_state'])
            self.model.fit(X_train_scaled, y_train)
            
            # Predictions
            y_pred = self.model.predict(X_test_scaled)
            y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
            
            # Feature importance
            feature_importance = []
            for name, coef in zip(X.columns, self.model.coef_[0]):
                feature_importance.append({
                    'feature': name,
                    'coefficient': float(coef),
                    'abs_importance': float(abs(coef))
                })
            
            # Sort by absolute importance
            feature_importance.sort(key=lambda x: x['abs_importance'], reverse=True)
            
            # Cross validation
            cv_scores = cross_val_score(
                self.model, X_train_scaled, y_train,
                cv=ANALYSIS_PARAMS['cv_folds']
            )
            
            results = {
                'feature_importance': feature_importance,
                'classification_report': classification_report(y_test, y_pred),
                'roc_auc': roc_auc_score(y_test, y_pred_proba),
                'cv_scores': {
                    'mean': float(cv_scores.mean()),
                    'std': float(cv_scores.std()),
                    'scores': cv_scores.tolist()
                }
            }
            
            logger.info("Logistic regression analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in logistic regression analysis: {str(e)}")
            raise AnalysisError(f"Logistic regression failed: {str(e)}")
    
    def test_strategy_effectiveness(self, paths_df):
        """
        Test effectiveness of different navigation strategies
        
        Parameters:
        -----------
        paths_df : pd.DataFrame
            DataFrame containing path information and strategies
            
        Returns:
        --------
        dict
            Test results and statistics
        """
        try:
            logger.info("Testing strategy effectiveness...")
            
            # Create contingency table
            contingency = pd.crosstab(paths_df['strategy'], paths_df['success'])
            
            # Chi-square test
            chi2, p_value, dof, expected = chi2_contingency(contingency)
            
            # Calculate Cramer's V for effect size
            n = contingency.sum().sum()
            min_dim = min(contingency.shape) - 1
            cramer_v = np.sqrt(chi2 / (n * min_dim))
            
            # Success rates by strategy
            success_rates = paths_df.groupby('strategy')['success'].agg(['mean', 'count'])
            
            results = {
                'test_name': 'Strategy Effectiveness Test',
                'chi2': chi2,
                'p_value': p_value,
                'dof': dof,
                'effect_size': cramer_v,
                'success_rates': success_rates,
                'contingency_table': contingency
            }
            
            logger.info(f"Strategy effectiveness test completed: p-value = {p_value:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error in strategy effectiveness test: {str(e)}")
            raise AnalysisError(f"Strategy analysis failed: {str(e)}")
    
    def predict_success_probability(self, features):
        """
        Predict success probability for given features
        
        Parameters:
        -----------
        features : array-like
            Path features to predict on
            
        Returns:
        --------
        float
            Predicted probability of success
        """
        if self.model is None:
            raise AnalysisError("Model not fitted. Call fit_logistic_regression first.")
        
        try:
            # Scale features
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            
            # Predict probability
            prob = self.model.predict_proba(features_scaled)[0, 1]
            return prob
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise AnalysisError(f"Prediction failed: {str(e)}")


# How to use
# from src.statistical_tests import StatisticalAnalyzer

# # Initialize analyzer
# stat_analyzer = StatisticalAnalyzer()

# # Test semantic proximity hypothesis
# semantic_results = stat_analyzer.test_semantic_proximity_hypothesis(
#     paths_df, semantic_distances
# )

# # Fit logistic regression and analyze features
# model_results = stat_analyzer.fit_logistic_regression(paths_df)

# # Test strategy effectiveness
# strategy_results = stat_analyzer.test_strategy_effectiveness(paths_df)

# # Print significant features
# significant_features = model_results['feature_importance'][
#     model_results['feature_importance']['p_value'] < 0.05
# ]
# print("Significant predictors of success:")
# print(significant_features)
