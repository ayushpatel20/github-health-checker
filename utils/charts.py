import plotly.express as px
import pandas as pd

def create_issue_ratio_chart(open_issues: int, closed_issues: int):
    """
    Creates a pie chart comparing open vs closed issues.
    """
    if open_issues == 0 and closed_issues == 0:
        df = pd.DataFrame({'Status': ['No Issues'], 'Count': [1]})
        fig = px.pie(df, values='Count', names='Status', color_discrete_sequence=['#ced4da'])
    else:
        df = pd.DataFrame({
            'Status': ['Open Issues', 'Closed Issues'],
            'Count': [open_issues, closed_issues]
        })
        fig = px.pie(df, values='Count', names='Status', color='Status',
                     color_discrete_map={'Open Issues': '#ff6b6b', 'Closed Issues': '#51cf66'})
    
    fig.update_layout(
        title="Issues Status",
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    return fig

def create_metric_bar_chart(metrics: dict):
    """
    Creates a simple horizontal bar chart for quick metrics overview.
    """
    df = pd.DataFrame({
        'Metric': list(metrics.keys()),
        'Count': list(metrics.values())
    })
    
    fig = px.bar(df, x='Count', y='Metric', orientation='h', color_discrete_sequence=['#339af0'])
    
    fig.update_layout(
        title="Repository Stats Overview",
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
        xaxis_title="Count",
        yaxis_title=""
    )
    
    # If all metrics are 0, force the x-axis to a reasonable range so it doesn't look broken
    if sum(metrics.values()) == 0:
        fig.update_xaxes(range=[0, 10])
        
    return fig
