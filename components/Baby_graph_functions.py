import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import pickle
import shap
import plotly.tools as tls
from components.Baby_Function import shap_to_uri
from dash import html

def make_pie(data, col, select_value): 

    labels = data[col]
    values = data['freq']
    preg_perc = round(data['임신 성공 확률'] * 100, 2)

    pulls = [0.1 if label == select_value else 0 for label in labels]
    colors = ['#E95420' if label == select_value else '#FADCD9' for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        customdata=preg_perc,
        pull=pulls,
        showlegend=False,
        textposition='inside',
        hoverinfo='label+value+percent',
        hole=0.5,
        marker_colors=colors,
        name="",
        hovertemplate=['<b>Label: %{label}</b><br>빈도 비율: %{percent}<br>해당 구간 임신 성공 확률: %{customdata}%' if label == select_value else None for label in labels],
        texttemplate=['<b>%{label}</b><br>%{percent}' if label == select_value else None for label in labels],
    )]
    )

    fig.update_layout(
                    title_x = 0.5,
                    title_xanchor = 'center',
                    title_font_color = 'black',
                    title_font_family = 'NanumSquare',
                    coloraxis_showscale=False,
                    template='simple_white')

    return fig

def make_bar(data, col, select_value):
    labels = data[col]
    values = data['임신 성공 확률']
    counts = data['freq']


    colors = ['#E95420' if label == select_value else '#FADCD9' for label in labels]

    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        customdata=counts,
        text=values,
        textposition='auto',
        marker_color=colors,
        name="",
        hovertemplate=['<b>Label: %{x}</b><br>Percent: %{y:.2f}%<br>Count: %{customdata}' if label == select_value else None for label in labels],
        texttemplate=['<b>%{text:.2f}%</b>' if label == select_value else None for label in labels],
    )])

    fig.update_layout(
                title_x = 0.5,
                title_xanchor = 'center',
                title_font_color = 'black',
                title_font_family = 'NanumSquare',
                yaxis_title='임신 성공 확률',
                coloraxis_showscale=False,
                template='simple_white')

    return fig