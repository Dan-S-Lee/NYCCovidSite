import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly
from lxml import etree as ET
from lxml.html import builder as E
import lxml.html
from io import StringIO, BytesIO
import scipy.stats
#import dash
#import dash_table
#import dash_table.FormatTemplate as FormatTemplate

#importing all data from DOH Github
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

#create table

table_tag = E.TBODY()
table_tag.attrib['id'] = 'table_list'
i = 0
for ind, row in city_dfs['zipcode'].iterrows():
    th_element = E.TH(str(ind))
    th_element.attrib['scope'] = 'row'
    table_tag.insert(i,
        E.TR(
            th_element,
            E.TD(str('{:,.0f}'.format(row['COVID_CASE_COUNT']))),
            E.TD(str('{:,.0f}'.format(row['COVID_DEATH_COUNT']))),
            E.TD(str('{:,.2f}'.format(row['PERCENT_POSITIVE']))),
            E.TD(str('{:,.0f}'.format(row['POP_DENOMINATOR'])))
                         )
                    )
    i += 1

city_row = city_dfs['by-borough'][city_dfs['by-borough']['Borough'] == 'Citywide']
n_cases = city_row['Case Count'].values.tolist()[0]
n_deaths = city_row['Death Count'].values.tolist()[0]
n_avg = city_dfs['trends'].iloc[-1]['CASE_COUNT_7DAY_AVG']

date_updated = city_dfs['summary'].iloc[-1]['Number']

html_file = r'/home/SleepingTuna/NYCCovid/app/templates/home.html'

parser = ET.HTMLParser()
tree = ET.parse(html_file, parser)
result = ET.tostring(tree, pretty_print=True)

cases_elmt = tree.xpath("//h5[@id='total_cases']")[0]
deaths_elmt = tree.xpath("//h5[@id='total_deaths']")[0]
avg_elmt = tree.xpath("//h5[@id='total_avg']")[0]

date_elmt = tree.xpath("//h6[@id='updated_last']")[0]

cases_elmt.text = str('{:,.0f}'.format(n_cases))
deaths_elmt.text = str('{:,.0f}'.format(n_deaths))
avg_elmt.text = str('{:,.0f}'.format(n_avg))

date_elmt.text = 'Updated: ' + date_updated

table_result = tree.xpath("//tbody[@id='table_list']")[0]

parent = table_result.getparent()
parent.remove(table_result)
parent.insert(1, table_tag)

with open(r'/home/SleepingTuna/NYCCovid/app/templates/home.html', 'w') as f:
    f.write(lxml.html.tostring(tree, pretty_print=True).decode('utf-8'))


print("Data updated successfully with data from {}".format(date_updated))
