from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .data_processing import get_data

city_dfs = get_data()
available_indicators = ['Case', 'Hospitalization', 'Death', 'Trends']
date_ind = [i for i in range(len(city_dfs['trends']['date_of_interest'].values))]

layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='metric',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Case'
            ),
            dcc.RadioItems(
                id='metric-type',
                options=[{'label': i, 'value': i} for i in ['Count', 'Rate']],
                value='Count',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'max-height': '545px', 'width': '48%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='indicator-graphic', responsive=True),

    dcc.RangeSlider(
        id='year--slider',
        min=date_ind[0],
        max=date_ind[-1],
        value=[date_ind[0], date_ind[-1]],
        marks={date_ind[i]: str(dt) for i, dt in zip(date_ind, city_dfs['trends']['date_of_interest'].values.tolist())
               if datetime.strptime(dt, '%m/%d/%Y').day == 1}
    )
], style={'maxHeight':'545px'})
