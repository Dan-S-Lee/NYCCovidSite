from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data_processing import get_data

fig_dict = get_data()
available_indicators = [key for key in fig_dict.keys()]

layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='metric',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=available_indicators[0]
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='indicator-graphic')
])
