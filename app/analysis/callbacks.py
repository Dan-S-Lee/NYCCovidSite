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

def register_callbacks(dashapp):
    @dashapp.callback(
        Output('indicator-graphic', 'figure'),
        Input('metric', 'value'))
    def update_graph(metric):
        fig = fig_dict[metric]

        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, hovermode='closest',
                          font_family='Frank Ruhl Libre')

        return fig

