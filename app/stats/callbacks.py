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


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('indicator-graphic', 'figure'),
        Input('metric', 'value'),
        Input('metric-type', 'value'),
        Input('year--slider', 'value'))
    def update_graph(metric,
                     metric_type,
                     year_value):

        df = city_dfs['by-borough'].copy()

        if metric == 'Trends':
            min_date = city_dfs['trends'].iloc[year_value[0]]['date_time']
            max_date = city_dfs['trends'].iloc[year_value[1]]['date_time']
            df = city_dfs['trends-melt'].copy()
            df = df[(df['date_time'] >= min_date) & (df['date_time'] <= max_date)]

        col_name = metric + ' ' + metric_type

        if metric != 'Trends':
            fig = px.bar(df.iloc[0:5], x='Borough',
                         y=col_name,
                         title=col_name + ' by Borough', color_continuous_scale='Oranges',
                         color_discrete_sequence=['#FD6E4E'] * len(df.iloc[0:5])
                         )
            fig.update_layout(title={'x': 0.5,
                                     'xanchor': 'center'},
                              font=dict(family='Frank Ruhl Libre', size=14, color='#000000'),
                              legend=dict(
                                  yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                              ))
        else:
            fig = px.line(df, x='Date', y="Values", color="Metric")
            fig.update_layout(title={'text': 'City-wide Trends',
                                     'x': 0.5,
                                     'xanchor': 'center'},
                              font=dict(family='Frank Ruhl Libre', size=14, color='#000000'),
                              legend=dict(
                                  yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                              ))

        fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, hovermode='closest', font_family='Frank Ruhl Libre')

        return fig
