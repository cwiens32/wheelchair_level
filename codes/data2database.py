# -*- coding: utf-8 -*-
"""
data2database
    Load and transfer logsheet, subject dimensions, digitized, and force data
        to database.

This code will also create a table that records the table names of each cycle.

Created on Tue Jul 14 09:15:24 2020

@author: cwiens
"""

import sqlite3
import pandas as pd
import glob, os

from codes.importlogsheet import readls


""" set file names """
db = '../data/wc_level.sqlite'
logsheet = '../data/logsheet_master.xlsx'
sub_dim_file = '../data/Subject Body Dimensions_Complete2.xlsx'
wc_adj_file = '../data/wc-adjustments.xlsx'
results_file = '../data/DOD_graded_results_CW_200826.xlsx'


""" establish database connection """
conn = sqlite3.connect(db)


""" load master logsheet, subject dimensions, and WC adjustments """
ls = readls(logsheet)
sub_dim = pd.read_excel(sub_dim_file).iloc[:,:-1]
wc_adj = pd.read_excel(wc_adj_file, sheet_name = 'adj_stats')
results = pd.read_excel(results_file)


""" upload logsheet, subject dimensions, WC adjustments, and results files to database """
ls.to_sql('logsheet', conn, if_exists='replace', index=False)
sub_dim.to_sql('subject_dimensions', conn, if_exists='replace', index=False)
wc_adj.to_sql('wheelchair_adjustments', conn, if_exists='replace', index=False)
results.to_sql('results', conn, if_exists='replace', index=False)


""" load digitized and force data """
# intialzie table_data
table_data = None
# change folder to where data is stored
os.chdir('../data/subject_data')
# loop through each file
for file in glob.glob('*.xlsx'):
    data_angle = pd.read_excel(file, sheet_name = "Sheet1")
    data_rf = pd.read_excel(file, sheet_name = "Sheet2")
    # find cycle info
    sub = '{:02}'.format(int(''.join(filter(str.isdigit, file[:7]))))
    sess = ''.join(filter(str.isdigit, file[10:18]))
    cond = ''.join(filter(str.isdigit, file[22:28]))
    trial = '{:02}'.format(int(''.join(filter(str.isdigit, file[28:37]))))
    cycle = '{:02}'.format(int(''.join(filter(str.isdigit, file[36:]))))
    """ upload all data to database """
    data_angle.to_sql('angle_' + sub + sess + cond + trial + cycle, conn, if_exists='replace')
    data_rf.to_sql('force_' + sub + sess + cond + trial + cycle, conn, if_exists='replace')
    """ add data info to list of tables """
    if table_data is None:
        table_data = pd.DataFrame({'subject_id': [int(sub)],
                                   'session': [int(sess)],
                                   'condition': [int(cond)],
                                   'trial': [int(trial)],
                                   'cycle': [int(cycle)],
                                   'force': ['force_' + sub + sess + cond + trial + cycle],
                                   'angle': ['angle_' + sub + sess + cond + trial + cycle]})
    else:
        table_data = table_data.append(pd.DataFrame({'subject_id': [int(sub)],
                                                     'session': [int(sess)],
                                                     'condition': [int(cond)],
                                                     'trial': [int(trial)],
                                                     'cycle': [int(cycle)],
                                                     'force': ['force_' + sub + sess + cond + trial + cycle],
                                                     'angle': ['angle_' + sub + sess + cond + trial + cycle]})).reset_index(drop=True)
            
# return to original folder
os.chdir('../..')
# upload table_data
table_data.to_sql('table_list', conn, if_exists='replace', index=False)


""" close connection """
conn.close()
