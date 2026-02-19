"""
Data Manager Module
Handles CSV import, validation, and data summary statistics
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional


def load_csv_file(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Load a CSV file and return DataFrame and error message.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Tuple of (DataFrame, error_message)
        If successful: (df, None)
        If error: (None, error_message)
    """
    try:
        df = pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, str(e)


def validate_rcbd_data(
    df: pd.DataFrame,
    treatment_col: str,
    rep_col: str,
    response_col: str
) -> Tuple[bool, str]:
    """
    Validate RCBD data structure.

    Args:
        df: Input DataFrame
        treatment_col: Name of treatment/genotype column
        rep_col: Name of replication/block column
        response_col: Name of response/yield column

    Returns:
        Tuple of (is_valid, message)
    """
    errors = []

    # Check if columns exist
    for col in [treatment_col, rep_col, response_col]:
        if col not in df.columns:
            errors.append(f"❌ คอลัมน์ '{col}' ไม่พบในข้อมูล")

    if errors:
        return False, "\n".join(errors)

    # Check for null values
    for col in [treatment_col, rep_col, response_col]:
        if df[col].isnull().any():
            null_count = df[col].isnull().sum()
            errors.append(f"⚠️ คอลัมน์ '{col}' มีค่าว่าง {null_count} ตำแหน่ง")

    # Check if response is numeric
    if not pd.api.types.is_numeric_dtype(df[response_col]):
        errors.append(f"❌ คอลัมน์ '{response_col}' ต้องเป็นตัวเลข")

    if errors:
        return False, "\n".join(errors)

    return True, "✅ ข้อมูลถูกต้องสำหรับการวิเคราะห์ RCBD"


def get_summary_stats(
    df: pd.DataFrame,
    response_col: str,
    treatment_col: Optional[str] = None
) -> Dict:
    """
    Calculate summary statistics for response variable.

    Args:
        df: Input DataFrame
        response_col: Name of response column
        treatment_col: Optional treatment column for grouped stats

    Returns:
        Dictionary of summary statistics
    """
    response_data = df[response_col].dropna()

    stats = {
        "n": len(response_data),
        "mean": response_data.mean(),
        "std": response_data.std(),
        "se": response_data.sem(),
        "min": response_data.min(),
        "max": response_data.max(),
        "q25": response_data.quantile(0.25),
        "median": response_data.quantile(0.50),
        "q75": response_data.quantile(0.75),
    }

    # Grouped stats if treatment column provided
    if treatment_col is not None and treatment_col in df.columns:
        grouped = df.groupby(treatment_col)[response_col].agg([
            ('n', 'count'),
            ('mean', 'mean'),
            ('std', 'std'),
            ('min', 'min'),
            ('max', 'max'),
        ])
        stats['grouped'] = grouped

    return stats


def get_design_info(
    df: pd.DataFrame,
    treatment_col: str,
    rep_col: str
) -> Dict:
    """
    Get experimental design information from data.

    Args:
        df: Input DataFrame
        treatment_col: Name of treatment column
        rep_col: Name of replication column

    Returns:
        Dictionary with design info
    """
    num_treatments = df[treatment_col].nunique()
    num_reps = df[rep_col].nunique()
    total_plots = len(df)

    design_info = {
        "num_treatments": num_treatments,
        "num_reps": num_reps,
        "total_plots": total_plots,
        "expected_plots": num_treatments * num_reps,
        "is_balanced": total_plots == (num_treatments * num_reps),
    }

    return design_info


def clean_data(
    df: pd.DataFrame,
    response_col: str,
    remove_outliers: bool = False,
    threshold: float = 3.0
) -> pd.DataFrame:
    """
    Clean data by removing nulls and optionally outliers.

    Args:
        df: Input DataFrame
        response_col: Name of response column
        remove_outliers: Whether to remove outliers
        threshold: Standard deviations for outlier detection (default 3.0)

    Returns:
        Cleaned DataFrame
    """
    # Remove nulls
    df_clean = df.dropna(subset=[response_col])

    # Remove outliers if requested
    if remove_outliers:
        mean = df_clean[response_col].mean()
        std = df_clean[response_col].std()
        lower_bound = mean - threshold * std
        upper_bound = mean + threshold * std
        df_clean = df_clean[
            (df_clean[response_col] >= lower_bound) &
            (df_clean[response_col] <= upper_bound)
        ]

    return df_clean


def export_data_csv(df: pd.DataFrame, filename: str = "export_data.csv") -> bytes:
    """
    Export DataFrame to CSV bytes for download.

    Args:
        df: Input DataFrame
        filename: Name for export

    Returns:
        CSV as bytes
    """
    return df.to_csv(index=False).encode('utf-8')


def export_data_excel(df: pd.DataFrame, filename: str = "export_data.xlsx") -> bytes:
    """
    Export DataFrame to Excel bytes for download.

    Args:
        df: Input DataFrame
        filename: Name for export

    Returns:
        Excel as bytes
    """
    from io import BytesIO
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    return output.getvalue()
