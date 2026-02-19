"""
Visualization Module
Creates interactive charts using Plotly
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


def create_means_bar_chart(
    means_df: pd.DataFrame,
    title: str = "Treatment Means",
    x_label: str = "Treatment",
    y_label: str = "Mean Response"
) -> go.Figure:
    """
    Create interactive bar chart of treatment means.

    Args:
        means_df: DataFrame with treatment means (index = treatment, column 'Mean')
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Plotly Figure object
    """
    means_df_reset = means_df.reset_index()

    fig = px.bar(
        means_df_reset,
        x=means_df_reset.columns[0],
        y='Mean',
        title=title,
        labels={
            means_df_reset.columns[0]: x_label,
            'Mean': y_label
        },
        color=means_df_reset.columns[0],
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        hovermode='x unified',
        height=500,
        showlegend=False,
        font=dict(size=12)
    )

    return fig


def create_box_plot(
    df: pd.DataFrame,
    treatment_col: str,
    response_col: str,
    title: str = "Distribution by Treatment",
    x_label: str = "Treatment",
    y_label: str = "Response"
) -> go.Figure:
    """
    Create box plot showing response distribution by treatment.

    Args:
        df: Input DataFrame
        treatment_col: Column name for treatments
        response_col: Column name for response
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Plotly Figure object
    """
    fig = px.box(
        df,
        x=treatment_col,
        y=response_col,
        title=title,
        labels={
            treatment_col: x_label,
            response_col: y_label
        },
        color=treatment_col,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        hovermode='x unified',
        height=500,
        showlegend=False,
        font=dict(size=12)
    )

    return fig


def create_violin_plot(
    df: pd.DataFrame,
    treatment_col: str,
    response_col: str,
    title: str = "Distribution by Treatment (Violin)",
    x_label: str = "Treatment",
    y_label: str = "Response"
) -> go.Figure:
    """
    Create violin plot for detailed distribution visualization.

    Args:
        df: Input DataFrame
        treatment_col: Column name for treatments
        response_col: Column name for response
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Plotly Figure object
    """
    fig = px.violin(
        df,
        x=treatment_col,
        y=response_col,
        title=title,
        labels={
            treatment_col: x_label,
            response_col: y_label
        },
        color=treatment_col,
        color_discrete_sequence=px.colors.qualitative.Set2,
        box=True,
        points="outliers"
    )

    fig.update_layout(
        hovermode='x unified',
        height=500,
        showlegend=False,
        font=dict(size=12)
    )

    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    treatment_col: Optional[str] = None,
    title: str = "Scatter Plot",
    x_label: str = "X",
    y_label: str = "Y"
) -> go.Figure:
    """
    Create scatter plot.

    Args:
        df: Input DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        treatment_col: Optional column for color grouping
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Plotly Figure object
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=treatment_col if treatment_col else None,
        title=title,
        labels={
            x_col: x_label,
            y_col: y_label
        },
        color_discrete_sequence=px.colors.qualitative.Set2 if treatment_col else None
    )

    fig.update_layout(
        hovermode='closest',
        height=500,
        font=dict(size=12)
    )

    return fig


def create_means_with_error_bars(
    means_df: pd.DataFrame,
    title: str = "Treatment Means with SE",
    x_label: str = "Treatment",
    y_label: str = "Mean Response"
) -> go.Figure:
    """
    Create bar chart with error bars showing standard error.

    Args:
        means_df: DataFrame with 'Mean' and 'SE' columns
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        Plotly Figure object
    """
    means_df_reset = means_df.reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=means_df_reset.iloc[:, 0],
        y=means_df_reset['Mean'],
        error_y=dict(
            type='data',
            array=means_df_reset['SE'],
            visible=True
        ),
        marker=dict(
            color=means_df_reset['Mean'],
            colorscale='Viridis',
            showscale=False
        ),
        name='Mean ± SE',
        hovertemplate='<b>%{x}</b><br>Mean: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        hovermode='x unified',
        height=500,
        font=dict(size=12),
        showlegend=False
    )

    return fig


def create_gxe_heatmap(
    df: pd.DataFrame,
    genotype_col: str,
    environment_col: str,
    response_col: str,
    title: str = "GxE Heatmap"
) -> go.Figure:
    """
    Create heatmap for Genotype x Environment interaction.

    Args:
        df: Input DataFrame with genotypes, environments, responses
        genotype_col: Column name for genotypes
        environment_col: Column name for environments
        response_col: Column name for response values
        title: Chart title

    Returns:
        Plotly Figure object
    """
    # Create pivot table
    pivot_data = df.pivot_table(
        values=response_col,
        index=genotype_col,
        columns=environment_col,
        aggfunc='mean'
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlGn',
        hovertemplate='<b>%{y}</b> × %{x}<br>Response: %{z:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title=environment_col,
        yaxis_title=genotype_col,
        height=600,
        font=dict(size=12)
    )

    return fig


def create_qq_plot(
    residuals: pd.Series,
    title: str = "Q-Q Plot (Residuals)"
) -> go.Figure:
    """
    Create Q-Q plot for normality check.

    Args:
        residuals: Series of residuals
        title: Chart title

    Returns:
        Plotly Figure object
    """
    from scipy import stats

    residuals_sorted = residuals.sort_values()
    theoretical_quantiles = stats.norm.ppf((pd.Series(range(1, len(residuals) + 1)) - 0.5) / len(residuals))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=residuals_sorted.values,
        mode='markers',
        marker=dict(size=6, color='blue'),
        name='Residuals'
    ))

    # Add diagonal line
    min_val = min(theoretical_quantiles.min(), residuals_sorted.min())
    max_val = max(theoretical_quantiles.max(), residuals_sorted.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        name='Reference Line',
        line=dict(dash='dash', color='red')
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Theoretical Quantiles',
        yaxis_title='Sample Quantiles',
        height=500,
        font=dict(size=12)
    )

    return fig
