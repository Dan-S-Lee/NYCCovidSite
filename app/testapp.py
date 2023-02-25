from datetime import datetime
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

city_dfs = {}
city_dfs['by-borough'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-boro.csv')
city_dfs['by-age'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-age.csv')
city_dfs['by-sex'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-sex.csv')
city_dfs['hosp-trends'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/group-hosp-by-boro.csv')
city_dfs['summary'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/summary.csv', names = ['Metric', 'Number'], skiprows=1)
city_dfs['zipcode'] = pd.read_csv(r'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv', index_col = 'MODIFIED_ZCTA')
city_dfs['trends'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/data-by-day.csv')

city_dfs['by-borough'].columns = ['Borough', 'Case Rate', 'Hospitalization Rate', 'Death Rate', 'Case Count', 'Hospitalization Count', 'Death Count']
city_dfs['by-age'].columns = ['Age Group', 'Cases Rate', 'Hospitalization Rate', 'Death Rate', 'Case Count', 'Hospitalized Count', 'Death Count']
city_dfs['by-sex'].columns = ['Sex', 'Cases Rate', 'Hospitalization Rate', 'Death Rate', 'Case Count', 'Hospitalized Count', 'Death Count']
city_dfs['hosp-trends'].columns = ['Group',
                                   'Subgroup',
                                   'Brooklyn Hosp Count',
                                   'Brooklyn Hosp Rate',
                                   'Bronx Hosp Count',
                                   'Bronx Hosp Rate',
                                   'Manhattan Hosp Count',
                                   'Manhattan Hosp Rate',
                                   'Queens Hosp Count',
                                   'Queens Hosp Rate',
                                   'Staten Island Hosp Count',
                                   'Staten Island Hosp Rate']

city_dfs['by-borough']['Borough'] = city_dfs['by-borough']['Borough'].str.replace('StatenIsland', 'Staten Island')

city_dfs['trends']['date_time'] = pd.to_datetime(city_dfs['trends']['date_of_interest'], format='%m/%d/%Y')

city_dfs['trends-melt'] = pd.melt(city_dfs['trends'],
                                  id_vars=['date_of_interest', 'date_time'],
                                  value_vars=['CASE_COUNT', 'HOSPITALIZED_COUNT', 'DEATH_COUNT'])
city_dfs['trends-melt'].columns = ['Date', 'date_time', 'Metric', 'Values']

label_map = {"CASE_COUNT": "Case Count",
             "HOSPITALIZED_COUNT": "Hospitalized Count",
             "DEATH_COUNT": "Death Count"}
city_dfs['trends-melt']['Metric'] = city_dfs['trends-melt']['Metric'].map(label_map)

available_indicators = ['Case', 'Hospitalization', 'Death', 'Trends']

#date indexes for html
date_ind = [i for i in range(len(city_dfs['trends']['date_of_interest'].values))]

app.layout = html.Div([
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
        style={'width': '48%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.RangeSlider(
        id='year--slider',
        min=date_ind[0],
        max=date_ind[-1],
        value=[date_ind[0], date_ind[-1]],
        marks={date_ind[i]: str(dt) for i, dt in zip(date_ind, city_dfs['trends']['date_of_interest'].values.tolist())
               if datetime.strptime(dt, '%m/%d/%Y').day == 1}
    )
])

@app.callback(
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


if __name__ == '__main__':
    app.run_server(debug=True)