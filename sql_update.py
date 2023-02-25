# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:43:50 2020

@author: Daniel
"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import json
import os
import numpy as np
from lxml import etree as ET
from lxml.html import builder as E
import lxml.html


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

def table_update_sql(table_name, columns, conn):
    for col in columns:
        query = """UPDATE {0}
            SET {1} = (SELECT {1}
            FROM data_by_modzcta
            WHERE Zip = {0}.Zip)""".format(table_name, col)
        c = conn.cursor()
        try:
            c.execute(query)
        except:
            pass
        c.close()
    conn.commit()

conn = create_connection(r'/home/SleepingTuna/NYCCovid/app/nyc_data.db')
corona_data = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv')
corona_data['Zip'] = corona_data['MODIFIED_ZCTA'].fillna(0).astype(int)
corona_data.to_sql(name='data_by_modzcta', con=conn, if_exists='replace', index=False, index_label='Zip')

table_list = ['household_size_percent', 'median_income', 'race_percent', 'sex_by_age_percent', 'health_insurance']
col_names = corona_data.columns.values
for table in table_list:
    table_update_sql(table, col_names, conn)

conn.close()

city_dfs = {}
city_dfs['summary'] = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/summary.csv', names = ['Metric', 'Number'], skiprows=1)
date_updated = city_dfs['summary'].iloc[-1]['Number']

html_file = r'/home/SleepingTuna/NYCCovid/app/templates/statistics.html'

parser = ET.HTMLParser()
tree = ET.parse(html_file, parser)
result = ET.tostring(tree, pretty_print=True)
date_elmt = tree.xpath("//h6[@id='updated_last']")[0]

date_elmt.text = 'Updated: ' + date_updated

with open(r'/home/SleepingTuna/NYCCovid/app/templates/statistics.html', 'w') as f:
    f.write(lxml.html.tostring(tree, pretty_print=True).decode('utf-8'))

html_file = r'/home/SleepingTuna/NYCCovid/app/templates/home.html'

parser = ET.HTMLParser()
tree = ET.parse(html_file, parser)
result = ET.tostring(tree, pretty_print=True)
date_elmt = tree.xpath("//h6[@id='updated_last']")[0]
date_elmt.text = 'Updated: ' + date_updated

with open(r'/home/SleepingTuna/NYCCovid/app/templates/home.html', 'w') as f:
    f.write(lxml.html.tostring(tree, pretty_print=True).decode('utf-8'))

html_file = r'/home/SleepingTuna/NYCCovid/app/templates/regressions.html'

parser = ET.HTMLParser()
tree = ET.parse(html_file, parser)
result = ET.tostring(tree, pretty_print=True)
date_elmt = tree.xpath("//h6[@id='updated_last']")[0]

date_elmt.text = 'Updated: ' + date_updated

with open(r'/home/SleepingTuna/NYCCovid/app/templates/regressions.html', 'w') as f:
    f.write(lxml.html.tostring(tree, pretty_print=True).decode('utf-8'))

print('Data updated successfully.')