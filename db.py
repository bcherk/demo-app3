import mysql.connector
import pandas as pd
pd.options.display.width = 0
pd.set_option('display.max_columns',10)
import numpy as np



mydb = mysql.connector.connect(

    # host = '127.0.0.1',
    # user = 'bcherk',
    # port = "3333",
    # password = 'newpassword',
    # database = 'bcherk$revitdb')
    host = 'bcherk.mysql.pythonanywhere-services.com',
    user = 'bcherk',

    password = 'newpassword',
    database = 'bcherk$revitdb')

my_cursor = mydb.cursor()

### Query Section ###

my_cursor.execute(
"""
SELECT * FROM bcherk$revitdb.revit_sections;
""")

result = my_cursor.fetchall()
df_sections = pd.DataFrame(result)
df_sections.columns = my_cursor.column_names
print(df_sections)

### Query Section ###

my_cursor.execute(
"""
SELECT * FROM bcherk$revitdb.section_types_comparisson;
""")

result_1 = my_cursor.fetchall()
df_section_comprisson = pd.DataFrame(result_1)
df_section_comprisson.columns = my_cursor.column_names
df_section_comprisson['check'] = np.where(df_section_comprisson['crossectional_area_robot'] == df_section_comprisson['crossectional_area_revit'], True, False)
df_section_comprisson.head()

df_section_comprisson['check'] = df_section_comprisson['check'].apply(lambda x: '✔️' if x == True else '❌')
print(df_section_comprisson)
# -*- coding: utf-8 -*-



my_cursor.close()