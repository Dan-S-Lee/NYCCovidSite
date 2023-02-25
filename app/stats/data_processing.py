from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def get_data():
    city_dfs = {}
    city_dfs['by-borough'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-boro.csv')
    city_dfs['by-age'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-age.csv')
    city_dfs['by-sex'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-sex.csv')
    city_dfs['hosp-trends'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/group-hosp-by-boro.csv')
    city_dfs['summary'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/summary.csv', names = ['Metric', 'Number'], skiprows=1)
    city_dfs['zipcode'] = pd.read_csv(r'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv', index_col = 'MODIFIED_ZCTA')
    city_dfs['trends'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/data-by-day.csv')

    city_dfs['by-borough'].columns = ['Borough',
                                        'Confirmed Case Rate',
                                        'Case Rate',
                                        'Hospitalization Rate',
                                        'Death Rate',
                                        'Confirmed Case Count',
                                        'Probable Case Count',
                                        'Case Count',
                                        'Hospitalization Count',
                                        'Death Count']
    city_dfs['by-age'].columns = ['Age Group',
                                        'Confirmed Case Rate',
                                        'Case Rate',
                                        'Hospitalization Rate',
                                        'Death Rate',
                                        'Confirmed Case Count',
                                        'Probable Case Count',
                                        'Case Count',
                                        'Hospitalization Count',
                                        'Death Count']
    city_dfs['by-sex'].columns = ['Sex',
                                        'Confirmed Case Rate',
                                        'Case Rate',
                                        'Hospitalization Rate',
                                        'Death Rate',
                                        'Confirmed Case Count',
                                        'Probable Case Count',
                                        'Case Count',
                                        'Hospitalization Count',
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

    return city_dfs
