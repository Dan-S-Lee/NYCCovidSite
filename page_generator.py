import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
from lxml import etree as ET
from lxml.html import builder as E
import lxml.html
import scipy.stats
import dash
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

city_dfs = {}
city_dfs['by-borough'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-boro.csv')
city_dfs['by-age'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-age.csv')
city_dfs['by-sex'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-sex.csv')
city_dfs['hosp-trends'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/group-hosp-by-boro.csv')
city_dfs['summary'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/summary.csv', names = ['Metric', 'Number'], skiprows=1)
city_dfs['zipcode'] = pd.read_csv(r'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv', index_col = 'MODIFIED_ZCTA')

city_dfs['by-borough'].columns = ['Borough',
                                  'Cases Rate',
                                  'Hospitalization Rate',
                                  'Death Rate', 'Case Count',
                                  'Hospitalization Count',
                                  'Death Count']
city_dfs['by-age'].columns = ['Age Group',
                              'Cases Rate',
                              'Hospitalization Rate',
                              'Death Rate',
                              'Case Count',
                              'Hospitalized Count',
                              'Death Count']
city_dfs['by-sex'].columns = ['Sex',
                              'Cases Rate',
                              'Hospitalization Rate',
                              'Death Rate',
                              'Case Count',
                              'Hospitalized Count',
                              'Death Count']
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

#importing fonts
#external_stylesheets = [r"https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre&display=swap"]

df = city_dfs['by-borough'].copy()
df['Borough'] = df['Borough'].str.replace('StatenIsland', 'Staten Island')
app = dash.Dash(__name__)

app.layout = html.Div([html.Label('Filter Borough: '),
                       html.Select([html.Option(val, value=val) for val in df['Borough'].values]),
    dash_table.DataTable(
        id='datatable_summary',
        columns=[{"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'center', 'font-family': 'Frank Ruhl Libre'},
        style_as_list_view=True,
        sort_action="native",
    ),
    html.Div(id='datatable_summary_container')
])

# @app.callback(
#     Output(component_id)
# )

if __name__ == '__main__':
    app.run_server(debug=True)