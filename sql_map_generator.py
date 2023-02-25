# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:19:29 2020

@author: Daniel
"""

import pandas as pd
import folium
from folium import IFrame
import json
import folium.features as features
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import math
import sqlite3
from sqlite3 import Error

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

zip_data = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv')
zip_data.rename(columns = {'MODIFIED_ZCTA': 'zipcode', 'PERCENT_POSITIVE': '%_positive'}, inplace = True)
zip_data['Zip_str'] = zip_data['zipcode'].fillna(0).astype(int).astype(str)
zip_geo = f'/home/SleepingTuna/NYCCovid/data/zipcode_polygons.json'
conn = create_connection(r'/home/SleepingTuna/NYCCovid/app/nyc_data.db')

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

def create_tabbed_string(metrics: dict, demos: dict, stats: dict):
    page = ET.Element('html')
    html = ET.Element('body')
    page.append(html)
    w3_link = ET.Element('link',
                         attrib = {'rel' : 'stylesheet',
                                   'href' : r'https://dan-s-lee.github.io/NYCCovid/docs/css/w3.css'})
    w4_link = ET.Element('link',
                         attrib = {'rel' : 'stylesheet',
                                   'href' : r'static/css/w3.css',
                                   'type' : 'text/css'})
    font_link = ET.Element('link',
                           attrib= {'rel' : 'stylesheet', 'href': r'https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre&amp;display=swap'})

    covid_link = ET.Element('link',
                           attrib= {'rel' : 'stylesheet', 'href': r'static/css/covid.css'})

    style = ET.Element('style')
    style.text = r".w3-montserrat {font-family: 'Montserrat', sans-serif;} header {border-radius: 12px 12px 0px 0px}"

    html.append(w4_link)
    html.append(w3_link)
    html.append(font_link)
    html.append(covid_link)
    #html.append(style)

    header = ET.Element('header', attrib = {'class' : 'w3-container w3-red'})
    html.append(header)
    h = ET.Element('h4')
    h.text = 'Zip Code:' + ' ' + str(metrics['Zip Code:'])

    header.append(h)

    '''create buttons'''

    button_div = ET.Element('div', attrib = {'class': 'w3-bar w3-black'})
    html.append(button_div)

    button = ET.Element('button', attrib = {'class': 'w3-bar-item w3-button', 'onclick':"openTab('Summary')"})
    button.text = 'Summary'
    button_div.append(button)

    button = ET.Element('button', attrib = {'class': 'w3-bar-item w3-button', 'onclick':"openTab('Demo')"})
    button.text = 'Demographics'
    button_div.append(button)

    button = ET.Element('button', attrib = {'class': 'w3-bar-item w3-button', 'onclick':"openTab('Statistics')"})
    button.text = 'Statistics'
    button_div.append(button)

    '''container for the summary tab'''

    container = ET.Element('div', attrib = {'id':'Summary','class': 'w3-container table w3-padding-0'})
    html.append(container)

    table = ET.Element('table', attrib = {'class' : "w3-table w3-bordered"})
    container.append(table)

    body_keys = [k for k in metrics.keys() if k != 'Zip Code:']
    for k in body_keys:
        new_row = ET.Element('tr')
        name_cell = ET.Element('td')
        name_cell.text = k

        new_row.append(name_cell)

        value_cell = ET.Element('td')
        if k != 'Zip Code:':
            try:
                value_cell.text = f"{metrics[k]:,d}"
            except:
                value_cell.text = '{:,.2f}'.format(metrics[k])
        else:
            value_cell.text = str(metrics[k])

        new_row.append(value_cell)

        table.append(new_row)

    '''container for demographics tab'''

    demo_container = ET.Element('div', attrib = {'id':'Demo','class': 'w3-container table w3-padding-0', 'style' : 'display:none'})
    html.append(demo_container)

    table = ET.Element('table', attrib = {'class' : "w3-table w3-bordered w3-padding-0"})
    demo_container.append(table)

    tab_keys = [k for k in demos.keys()]
    for k in tab_keys:
        new_row = ET.Element('tr')
        if k == 'Race':
            name_cell = ET.Element('th')
            value_cell = ET.Element('th')
        else:
            name_cell = ET.Element('td')
            value_cell = ET.Element('td')
        #name_cell = ET.Element('td')
        name_cell.text = k

        new_row.append(name_cell)

        #value_cell = ET.Element('td')
        if not demos[k] == 'Percentage':
            value_cell.text = str(demos[k])
        else:
            value_cell.text = demos[k]

        new_row.append(value_cell)

        table.append(new_row)

    '''container for the stats tab'''

    container = ET.Element('div', attrib = {'id':'Statistics','class': 'w3-container table w3-padding-0', 'style' : 'display:none'})
    html.append(container)

    table = ET.Element('table', attrib = {'class' : "w3-table w3-bordered"})
    container.append(table)

    stat_keys = [k for k in stats.keys()]
    for k in stat_keys:
        new_row = ET.Element('tr')
        name_cell = ET.Element('td')
        name_cell.text = k

        new_row.append(name_cell)

        value_cell = ET.Element('td')
        if k == 'Median Income:':
            value_cell.text = '$' + '{:,.0f}'.format(int(stats[k]))
        elif k == 'Poverty Rate:':
            value_cell.text = '{:,.1f}'.format(float(stats[k])) + '%'
        elif k != 'Zip Code:':
            try:
                value_cell.text = f"{stats[k]:,d}"
            except:
                value_cell.text = '{:,.2f}'.format(float(stats[k]))
        else:
            value_cell.text = str(stats[k])

        new_row.append(value_cell)

        table.append(new_row)

    script = ET.Element('script')
    script.text = 'function openTab(tabName) { var i;  var x = document.getElementsByClassName("table");  for (i = 0; i < x.length; i++) {    x[i].style.display = "none";  } document.getElementById(tabName).style.display = "block";  }'
    html.append(script)

    return ET.tostring(html)

def metrics_organizer(df_, categories, zc, val, symbol):
    '''
    pulls dataframe values based on categories at a given index

    inputs:
    df - Dataframe
    categories - dictionary used to rename column while preserving dataframe naming scheme
    zc - zipcode
    val - actual row of df at given ind
    symbol - symbol to append at each value

    returns:
    metrics - dictionary to feed into string-generator
    '''
    metrics = {}
    for key in categories.keys():
        metrics[key] = str(df_.query('Zip == {}'.format(zc)).iloc[0][categories[key]]) + ' '+ symbol
    return metrics

m = folium.Map(location = [40.7128, -74.0060], zoom_start = 12)
zip_geo = f'/home/SleepingTuna/NYCCovid_old/data/zipcode_polygons.json'
style = {'fillColor': '#00000000', 'lineColor': '#00FFFFFF'}
#zipcode_layer = folium.GeoJson(zip_geo, style_function = lambda x: style).add_to(m)
zc_layer = folium.Choropleth(
geo_data=zip_geo,
name = 'choropleth',
data = zip_data[0:],
columns = ['Zip_str', 'COVID_CASE_RATE'],
key_on = 'feature.properties.postalCode',
fill_color='YlOrBr',
fill_opacity=0.7,
line_opacity=1.0,
legend_name='Infection Rate',
).add_to(m)
#tip = features.GeoJsonTooltip(fields = ['postalCode']).add_to(zipcode_layer)

df = df_dict['data_by_modzcta']
income_df = df_dict['median_income']
household_df = df_dict['household_size_percent']
poverty_df = df_dict['poverty']

for i, v in df.iterrows():
    missing = False
    metrics_dict = {}
    metrics_dict['Zip Code:'] = df.loc[i]['Zip']

    metrics_dict['Tested Positive:'] = df.loc[i]['COVID_CASE_COUNT']
    metrics_dict['Per 100,000:'] = df.loc[i]['COVID_CASE_RATE']

    metrics_dict['Population:'] = int(round(df.loc[i]['POP_DENOMINATOR']))

    stats_dict = {}
    try:
        stats_dict['Median Income:'] = income_df.query('Zip == {}'.format(df.loc[i]['Zip'])).iloc[0]['Median_household_income_(dollars)']
        stats_dict['WAVG Household Size:'] = household_df.query('Zip == {}'.format(df.loc[i]['Zip'])).iloc[0]['Weighted_Avg']
        stats_dict['Poverty Rate:'] = poverty_df.query('Zip == {}'.format(df.loc[i]['Zip'])).iloc[0]['Below_Poverty_Level_-_All_people']
    except:
        print(str(df.loc[i]['Zip']) + ' is missing')
        missing = True
    if not missing:
        demo_renaming = {'White':'White_alone',
                         'African American': 'Black_or_African_American_alone',
                         'Native American': 'American_Indian_and_Alaska_Native_alone',
                         'Asian': 'Asian_alone',
                         'Pacific Islander': 'Native_Hawaiian_and_Other_Pacific_Islander_alone',
                         'Other Races': 'Some_Other_Race_alone',
                         'Two or More Races': 'Two_or_More_Races'}

        demo_dict = {'Race' : 'Percentage'}
        demo_dict.update(metrics_organizer(df_dict['race_percent'], demo_renaming, metrics_dict['Zip Code:'], v, '%'))

        popup_text = create_tabbed_string(metrics_dict, demo_dict, stats_dict).decode().replace('&lt;', '<')
        iframe = IFrame(html=popup_text, width = '100%', height = 300)
        if i == 10001:
            sample = popup_text
        #print(popup_text)
        popup = folium.Popup(iframe, max_width = 375, min_width = 375)

        tooltip_text = '<b> ZipCode: </b>' + df.loc[i]['Zip'].astype(str) + ' <br/> Click for more info.'
        tooltip = folium.Tooltip(tooltip_text)

        icon = features.DivIcon(icon_size = (50,50), icon_anchor = (0,0), html = '<b>' + df.loc[i]['Zip'].astype(str) + '</b>')

        #folium.Circle(tuple(df.loc[i][['Latitude', 'Longitude']]), radius = float(min(math.log(metrics_dict['Per 100,000:']) * 150, 1000)), tooltip = tooltip, popup= popup, fill = True, fill_color = '#FF0000', color = '#FF0000', icon = icon).add_to(m)
        query_df = df_dict['nyc_zip_codes'].query('Zip == {}'.format(df.loc[i]['Zip']))
        query_df[['Latitude', 'Longitude']] = query_df[['Latitude', 'Longitude']].astype(float)
        if len(query_df):
            folium.Circle(tuple(query_df.iloc[0][['Latitude', 'Longitude']].values), radius = float(metrics_dict['Per 100,000:'])/50, tooltip = tooltip, popup= popup, fill = True, fill_color = '#FF0000', color = '#FF0000', icon = icon).add_to(m)

    #folium.map.Marker(tuple(data.iloc[i][['Latitude', 'Longitude']]), icon = icon).add_to(m)

m.save(r'/home/SleepingTuna/NYCCovid/app/templates/master.html')
soup = BeautifulSoup(open(r'/home/SleepingTuna/NYCCovid/app/templates/master.html'))
links = soup.findAll('link')
for link in links:
    link['href'] = link['href'].replace(r"https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css", "https://dan-s-lee.github.io/NYCCovid/docs/css/leaflet.css")
with open(r'/home/SleepingTuna/NYCCovid/app/templates/new_master.html', "w") as file:
    file.write(str(soup))

print('Map built successfully')