"""
ANOVA Module
Statistical analysis for experimental designs (RCBD, CRD, Latin Square)
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats


def run_rcbd_anova(
    df: pd.DataFrame,
    treatment_col: str,
    rep_col: str,
    response_col: str,
    alpha: float = 0.05
) -> Dict:
    """
    Perform RCBD (Randomized Complete Block Design) ANOVA.

    Args:
        df: Input DataFrame with data
        treatment_col: Column name for treatments (genotypes/varieties)
        rep_col: Column name for replications (blocks)
        response_col: Column name for response variable (yield)
        alpha: Significance level (default 0.05)

    Returns:
        Dictionary with ANOVA results including:
        - anova_table: ANOVA table as DataFrame
        - treatment_means: Mean for each treatment
        - cv: Coefficient of variation (%)
        - grand_mean: Grand mean of all observations
        - f_treatment: F-value for treatment
        - p_treatment: P-value for treatment
        - mse: Mean squared error
        - se: Standard error of difference
        - lsd: Least Significant Difference
    """
    # Ensure columns exist
    if treatment_col not in df.columns or rep_col not in df.columns or response_col not in df.columns:
        raise ValueError("One or more columns not found in DataFrame")

    # Create formula for RCBD
    # Response ~ C(Treatment) + C(Replication)
    formula = f"{response_col} ~ C({treatment_col}) + C({rep_col})"

    # Fit OLS model
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    # Extract results
    treatment_ss = anova_table.loc[f"C({treatment_col})", "sum_sq"]
    treatment_df = int(anova_table.loc[f"C({treatment_col})", "df"])
    treatment_ms = anova_table.loc[f"C({treatment_col})", "sum_sq"] / treatment_df
    treatment_f = anova_table.loc[f"C({treatment_col})", "F"]
    treatment_p = anova_table.loc[f"C({treatment_col})", "PR(>F)"]

    rep_ss = anova_table.loc[f"C({rep_col})", "sum_sq"]
    rep_df = int(anova_table.loc[f"C({rep_col})", "df"])

    residual_ss = anova_table.loc["Residual", "sum_sq"]
    residual_df = int(anova_table.loc["Residual", "df"])
    residual_ms = anova_table.loc["Residual", "sum_sq"] / residual_df

    total_ss = anova_table.loc["Residual", "sum_sq"] + treatment_ss + rep_ss
    total_df = treatment_df + rep_df + residual_df

    # Calculate summary statistics
    n_obs = len(df)
    grand_mean = df[response_col].mean()
    cv = (np.sqrt(residual_ms) / grand_mean) * 100

    # Treatment means
    treatment_means = df.groupby(treatment_col)[response_col].agg(['mean', 'std', 'count'])
    treatment_means.columns = ['Mean', 'Std', 'N']
    treatment_means['SE'] = treatment_means['Std'] / np.sqrt(treatment_means['N'])

    # Calculate LSD (Least Significant Difference)
    # LSD = t_alpha/2 * SE
    # SE = sqrt(2 * MSE / r) where r = number of replications
    num_reps = df[rep_col].nunique()
    se_diff = np.sqrt(2 * residual_ms / num_reps)
    t_critical = stats.t.ppf(1 - alpha / 2, residual_df)
    lsd = t_critical * se_diff

    # Formatted ANOVA table
    anova_formatted = pd.DataFrame({
        'Source': [treatment_col, rep_col, 'Residual', 'Total'],
        'df': [treatment_df, rep_df, residual_df, total_df],
        'Sum of Sq': [treatment_ss, rep_ss, residual_ss, total_ss],
        'Mean Sq': [treatment_ms, rep_ss / rep_df if rep_df > 0 else 0, residual_ms, total_ss / total_df if total_df > 0 else 0],
        'F-value': [treatment_f, np.nan, np.nan, np.nan],
        'Pr(>F)': [treatment_p, np.nan, np.nan, np.nan],
    })

    # Significance indicator
    is_significant = treatment_p < alpha

    results = {
        'anova_table': anova_formatted,
        'treatment_means': treatment_means,
        'cv': cv,
        'grand_mean': grand_mean,
        'f_treatment': treatment_f,
        'p_treatment': treatment_p,
        'is_significant': is_significant,
        'alpha': alpha,
        'mse': residual_ms,
        'se_diff': se_diff,
        'lsd': lsd,
        'model': model,
        'num_treatments': treatment_df + 1,
        'num_reps': num_reps,
        'residual_df': residual_df,
    }

    return results


def run_crd_anova(
    df: pd.DataFrame,
    treatment_col: str,
    response_col: str,
    alpha: float = 0.05
) -> Dict:
    """
    Perform CRD (Completely Randomized Design) ANOVA.

    Args:
        df: Input DataFrame with data
        treatment_col: Column name for treatments
        response_col: Column name for response variable
        alpha: Significance level

    Returns:
        Dictionary with ANOVA results
    """
    formula = f"{response_col} ~ C({treatment_col})"
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)

    treatment_f = anova_table.loc[f"C({treatment_col})", "F"]
    treatment_p = anova_table.loc[f"C({treatment_col})", "PR(>F)"]

    residual_ss = anova_table.loc["Residual", "sum_sq"]
    residual_df = int(anova_table.loc["Residual", "df"])
    residual_ms = residual_ss / residual_df

    grand_mean = df[response_col].mean()
    cv = (np.sqrt(residual_ms) / grand_mean) * 100

    treatment_means = df.groupby(treatment_col)[response_col].agg(['mean', 'std', 'count'])
    treatment_means.columns = ['Mean', 'Std', 'N']
    treatment_means['SE'] = treatment_means['Std'] / np.sqrt(treatment_means['N'])

    results = {
        'anova_table': anova_table,
        'treatment_means': treatment_means,
        'cv': cv,
        'grand_mean': grand_mean,
        'f_treatment': treatment_f,
        'p_treatment': treatment_p,
        'is_significant': treatment_p < alpha,
        'alpha': alpha,
        'mse': residual_ms,
        'model': model,
    }

    return results


def get_cv_quality(cv: float) -> str:
    """
    Classify CV (Coefficient of Variation) quality in Thai.

    Args:
        cv: Coefficient of Variation (%)

    Returns:
        Thai quality label
    """
    if cv < 10:
        return "ดีเยี่ยม (Excellent)"
    elif cv < 15:
        return "ดี (Good)"
    elif cv < 20:
        return "ยอมรับได้ (Acceptable)"
    else:
        return "ต่ำ (Poor)"


def get_significance_stars(p_value: float) -> str:
    """
    Get significance stars based on p-value.

    Args:
        p_value: P-value from test

    Returns:
        String with significance stars
    """
    if p_value < 0.001:
        return "***"
    elif p_value < 0.01:
        return "**"
    elif p_value < 0.05:
        return "*"
    else:
        return "ns"


def calculate_lsd(
    mse: float,
    num_reps: int,
    residual_df: int,
    alpha: float = 0.05
) -> float:
    """
    Calculate LSD (Least Significant Difference).

    Args:
        mse: Mean squared error from ANOVA
        num_reps: Number of replications
        residual_df: Degrees of freedom for residual
        alpha: Significance level

    Returns:
        LSD value
    """
    se = np.sqrt(2 * mse / num_reps)
    t_critical = stats.t.ppf(1 - alpha / 2, residual_df)
    return t_critical * se
