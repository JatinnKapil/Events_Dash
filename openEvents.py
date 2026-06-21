import datetime
import socket
import getpass
import os
import pyodbc
import re
import pandas as pd
import numpy as np
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

username = getpass.getuser()
name = os.getenv('username')
username = os.getlogin()
host = socket.gethostname()
print(
    f'\nHey {username} Welcome to Data Automation Program, This device name {host}\n')

print("\nclick link to continue for current events Data ")

print("or type CTRL C when you are finished: Data is running on  http://127.0.0.1:8050/ Chrome Browser \n")

cnxn = pyodbc.connect(Trusted_Connection='yes',
                      driver='{ODBC Driver 17 for SQL Server}', server='CALVS1210\MISCAPP', database='PCMSWIN')

sqlFile = open(
    r'H:\LPG Operations\Mechanical Integrity\FAI Team Folder\Jatinn\IntelliSense\open_events.sql', 'r')
myQuery = sqlFile.read()

xls_file = pd.read_sql_query(myQuery, cnxn, dtype='unicode')

# cnxn.close()


def whitespace_remover(xls_file):

    # iterating over the columns
    for i in xls_file.columns:

        # checking datatype of each columns
        if xls_file[i].dtype == 'object':

            # applying strip function on column
            xls_file[i] = xls_file[i].map(str.strip)
        else:

            # if condn. is False then it will do nothing.
            pass


# applying whitespace_remover function on dataframe
whitespace_remover(xls_file)
# printing dataframe
# print(xls_file)

# xls_file = pd.read_csv(r'H:\LPG Operations\Mechanical Integrity\FAI Team Folder\ITPs\ITP Data\itp_data_new.csv',
#                        encoding='ISO-8859-1', low_memory=False, dtype='unicode')

# xls_file = xls_file.replace(['None'], [''], regex=True)
# xls_file = xls_file.replace(['nan'], [''], regex=True)
# xls_file = xls_file.replace(['NaT'], [''], regex=True)
# xls_file.to_excel('testingInspectionEvents.xlsx',
#                   sheet_name='testingInspectionEvents', index=False)

# df = pd.read_excel("testingInspectionEvents.xlsx")
df = xls_file
df.rename(columns={'Event Type': 'Event_Type'}, inplace=True)

df = df[(df['Event_Type'] == 'External Inspection') | (df['Event_Type'] == 'Internal Inspection') | (df['Event_Type'] == 'NDT') | (df['Event_Type'] == 'On-Stream Inspection') |
        (df['Event_Type'] == 'Relief Valve Test/Repair') | (df['Event_Type'] == 'CUI Inspection') | (df['Event_Type'] == 'Corrosion Survey') | (df['Event_Type'] == 'Installation Inspection')]

df = df.reset_index()
table = pd.pivot_table(
    df, index=['Facility_ID'], columns=['Event_Type'], values=['Equipment_ID'], aggfunc=len, fill_value=0, margins=True, dropna=False)

# table = table.query(
#     'Event_Type != ["Failure","General Event","General Event-Incident","Relief Valve Test/Repair","Relief Valve Installation","Relief Valve Replacement","Installation Inspection"]')

# writer = pd.ExcelWriter(
#     'event.xlsx', engine='xlsxwriter')
# table.to_excel(writer, index=True, sheet_name='pivot_data')
# writer.save()
pv = table
mgr_options = df["Facility_ID"].unique()

# trace1 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 'External Inspection')], name='External Inspection')
# trace2 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 'Internal Inspection')], name='Internal Inspection')
# trace3 = go.Bar(x=pv.index, y=pv[(
#     'Equipment_ID', 'On-Stream Inspection')], name='On-Stream Inspection')
# trace4 = go.Bar(x=pv.index, y=pv[(
#     'Equipment_ID', 'Relief Valve Test/Repair')], name='Relief Valve Test/Repair')
# trace5 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 'CUI Inspection')], name='CUI Inspection')
# trace6 = go.Bar(x=pv.index,
#                 y=pv[('Equipment_ID', 'Corrosion Survey')], name='Corrosion Survey')
# trace7 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 'NDT')], name='NDT')

# trace8 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 'Installation Inspection')], name='Installation Inspection')

# trace1 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 1)], name='Jan')
# # trace2 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 2)], name='Feb')
# trace3 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 3)], name='March')
# trace4 = go.Bar(x=pv.index,
#                 y=pv[('Equipment_ID', 4)], name='April')
# trace5 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 5)], name='MAY')
# trace6 = go.Bar(x=pv.index,
#                 y=pv[('Equipment_ID', 6)], name='JUNE')
# trace7 = go.Bar(
#     x=pv.index, y=pv[('Equipment_ID', 7)], name='July')
# trace8 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 8)], name='Aug')
# trace9 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 9)], name='Sep')
# trace10 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 10)], name='Oct')
# trace11 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 11)], name='Nov')
# trace12 = go.Bar(x=pv.index, y=pv[('Equipment_ID', 12)], name='Dec')

fig = go.Figure()
fig.add_trace(go.Bar(
    x=pv.index, y=pv[('Equipment_ID', 'External Inspection')], name='External Inspection'), go.Bar(
    x=pv.index,  y=pv[('Equipment_ID', 'Internal Inspection')], name='Internal Inspection'))
fig.layout.title.text = "A Figure Specified By A Graph Object"


fig.show()


app = Dash(__name__)
app.layout = html.Div([
    html.H4('The time is: ' + str(datetime.datetime.now())),
    html.H1(children='Inspection Events 2022 '),
    html.Div(children=''' Current Events Funnel Report.'''),
    dcc.Clipboard(target_id="structure"),
    dcc.Graph(
        id='example-graph', figure=fig),
    html.Pre(
        id='structure',
        style={'width': '1200px', 'Height': '600px', 'display': 'inline-block'}
    ),

])

# def serve_layout():
#     return html.H1('The time is: ' + str(datetime.datetime.now()))


# app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=False)

print(f"Thanx {username}! You're done")
# app.run_server(debug=True, host='127.0.0.1', port=8050)
