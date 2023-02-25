from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
import scipy.stats
import sqlite3
from sqlite3 import Error

external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_spearmann(x, y, title, xaxis, yaxis):
    spear_r, p_val = scipy.stats.spearmanr(x, y)
    slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)
    line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r= {spear_r:.2f}, p= {p_val:.2f}      '
    layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')
    reg_fig = go.Figure()
    reg_fig.add_trace(go.Scatter(x=x, y=y, name='ZCTA XY Pairs      ', mode = 'markers'))
    reg_fig.add_trace(go.Scatter(x=x, y=intercept + slope * x, name=line, mode='lines'))
    reg_fig.update_layout(title = {'text': title,
                                     'x': 0.5,
                                     'xanchor': 'center'},
                            font = dict(family = 'Frank Ruhl Libre', size = 12, color = '#000000'),
                          xaxis_title=xaxis,
                          yaxis_title=yaxis,
                         legend_orientation="h",
                         legend=dict(
                                    x=0.5,
                                    y=1,
                                    traceorder="normal",
                                    font=dict(
                                        family="Frank Ruhl Libre",
                                        size=12,
                                        color="black"
                                    ),
                                    bgcolor="LightSteelBlue",
                                    bordercolor="Black",
                                    borderwidth=2
                                ))

    reg_fig.update_layout({'paper_bgcolor':'rgba(0,0,0,0)',
        'plot_bgcolor':'rgba(0,0,0,0)'})
    reg_fig.update_xaxes(automargin=True)
    reg_fig.update_yaxes(automargin=True)
    return reg_fig

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

zip_data = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv')
zip_data.rename(columns={'MODIFIED_ZCTA': 'zipcode', 'PERCENT_POSITIVE': '%_positive'}, inplace=True)
zip_data['Zip_str'] = zip_data['zipcode'].fillna(0).astype(int).astype(str)
conn = create_connection('nyc_data.db')
to_extract = ['HOUSEHOLD SIZE',
              'HOUSING UNITS',
              'RACE',
              'SEX BY AGE',
              'TOTAL POPULATION',
              'HOUSEHOLD SIZE Percentage',
              'RACE Percentage',
              'SEX BY AGE Percentage',
              'MEDIAN INCOME',
              'POVERTY' ]
table_list = ['household_size',
              'housing_units',
              'race',
              'sex_by_age',
              'total_population',
              'household_size_percent',
              'median_income',
              'race_percent',
              'sex_by_age_percent',
              'health_insurance',
              'poverty',
              'data_by_modzcta',
              'nyc_zip_codes']
df_dict = {}
for table in table_list:
    df_dict[table] = pd.read_sql_query("select * from {};".format(table), conn)

race_data = df_dict['race_percent'].copy()
demo_renaming = {'White':'White_alone',
                 'African American': 'Black_or_African_American_alone',
                 'Native American': 'American_Indian_and_Alaska_Native_alone',
                 'Asian': 'Asian_alone',
                 'Pacific Islander': 'Native_Hawaiian_and_Other_Pacific_Islander_alone',
                 'Other Races': 'Some_Other_Race_alone',
                 'Two or More Races': 'Two_or_More_Races'}

#Setting x and y vectors for race regressions
x_dict = {}
for k,v in demo_renaming.items():
    x_dict[k] = race_data[v]
y = race_data['COVID_CASE_RATE'] / 100

graph_dict = {}
fig_dict = {}
for k, v in x_dict.items():
    spear_r, p_val = scipy.stats.spearmanr(x_dict[k], y)
    slope, intercept, r, p, stderr = scipy.stats.linregress(x_dict[k], y)
    line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r= {spear_r:.2f}, p= {p_val:.2f}          '
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    reg_fig = go.Figure()
    reg_fig.add_trace(go.Scatter(x=x_dict[k], y=y, name='ZCTA XY Pairs      ', mode='markers'))
    reg_fig.add_trace(go.Scatter(x=x_dict[k], y=intercept + slope * x_dict[k], name=line, mode='lines'))
    reg_fig.update_layout(title={'text': k,
                                 'x': 0.5,
                                 'xanchor': 'center'},
                          font=dict(family='Frank Ruhl Libre', size=12, color='#000000'),
                          xaxis_title=k + ' (%)',
                          yaxis_title='Infected per 1,000',
                          legend_orientation="h",
                          legend=dict(
                              x=0.5,
                              y=1,
                              traceorder="normal",
                              font=dict(
                                  family="Frank Ruhl Libre",
                                  size=12,
                                  color="black"
                              ),
                              bgcolor="LightSteelBlue",
                              bordercolor="Black",
                              borderwidth=2
                          ))

    reg_fig.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)',
                           'plot_bgcolor': 'rgba(0,0,0,0)'})
    reg_fig.update_xaxes(automargin=True)
    reg_fig.update_yaxes(automargin=True)
    fig_dict[k] = reg_fig
    graph_dict[k] = plotly.offline.plot(reg_fig, include_plotlyjs=False, output_type='div')

income_data = df_dict['median_income'].copy()
x = income_data['Median_household_income_(dollars)']/1000
y = income_data['COVID_CASE_RATE'] / 100

title, xaxis, yaxis = 'Median Household Income', 'Median Household Income' + ' (In Thousands)', 'Infected per 1,000'
fig_dict['Median Income'] = create_spearmann(x, y, title, xaxis, yaxis)

household_data = df_dict['household_size_percent'].copy()
x = household_data['Weighted_Avg']
y = household_data['COVID_CASE_RATE'] / 100
title, xaxis, yaxis = 'WAVG Household Size', 'WAVG Household Size', 'Infected per 1,000'
fig_dict['Weighted Avg Household'] = create_spearmann(x, y, title, xaxis, yaxis)


available_indicators = [key for key in fig_dict.keys()]

#date indexes for html
date_ind = [i for i in range(len(city_dfs['trends']['date_of_interest'].values))]

app.layout = html.Div([
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

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('metric', 'value'))
def update_graph(metric):

    fig = fig_dict[metric]

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, hovermode='closest', font_family='Frank Ruhl Libre')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)