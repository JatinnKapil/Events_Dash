import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


#Reading From a Database
# Connect to sqlite db
db_file = os.path.join(os.path.dirname(wb.fullname), 'events.db')
engine = create_engine(r"sqlite:///{}".format(db_file))
  data = pd.read_sql(sql, engine)
  # Read query directly into a dataframe
  # Create SQL query
sql = 'SELECT * from table WHERE x="{}" AND date BETWEEN "{}" AND "{}"'.format()
  
# else
# Read in the data from Excel

df = pd.read_excel("data.xlsx")
df.rename(columns={'Event Type': 'Event_Type'}, inplace=True)
df = df[(df['Event_Type'] == 'External Inspection') | (df['Event_Type'] == 'Internal Inspection') | (
    df['Event_Type'] == 'NDT') | (df['Event_Type'] == 'On-Stream Inspection') | (df['Event_Type'] == 'UST Inspection')]

table = pd.pivot_table(
    df, index=['Facility ID'], columns=["Month"], values=['Equipment ID'], aggfunc=len, fill_value=0, margins=True)

# table = table.query(
#     'Event_Type != ["Failure","General Event","General Event-Incident","Relief Valve Test/Repair","Relief Valve Installation","Relief Valve Replacement","Installation Inspection"]')

writer = pd.ExcelWriter(
    'event.xlsx', engine='xlsxwriter')
table.to_excel(writer, index=True, sheet_name='pivot_data')
writer.save()
pv = table
mgr_options = df["Region ID"].unique()


trace1 = go.Bar(x=pv.index, y=pv[('Equipment ID', 1)], name='Jan')
trace2 = go.Bar(x=pv.index, y=pv[('Equipment ID', 2)], name='Feb')
trace3 = go.Bar(
    x=pv.index, y=pv[('Equipment ID', 3)], name='March')
trace4 = go.Bar(x=pv.index,
                y=pv[('Equipment ID', 4)], name='April')
trace5 = go.Bar(
    x=pv.index, y=pv[('Equipment ID', 5)], name='MAY')
trace6 = go.Bar(x=pv.index,
                y=pv[('Equipment ID', 6)], name='JUNE')
trace7 = go.Bar(
    x=pv.index, y=pv[('Equipment ID', 7)], name='July')
trace8 = go.Bar(x=pv.index, y=pv[('Equipment ID', 8)], name='Aug')
trace9 = go.Bar(x=pv.index, y=pv[('Equipment ID', 9)], name='Sep')
trace10 = go.Bar(x=pv.index, y=pv[('Equipment ID', 10)], name='Oct')
trace11 = go.Bar(x=pv.index, y=pv[('Equipment ID', 11)], name='Nov')
trace12 = go.Bar(x=pv.index, y=pv[('Equipment ID', 12)], name='Dec')

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Events 2020 Weekly Report'),
    html.Div(children=''' Nov 1_Weekly Events Funnel Report.'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12],
            'layout':
            go.Layout(title='Events Inspection', colorway=["#EF963B", "#EF533B"], hovermode="closest",
                      bargap=0.15, bargroupgap=0.1,  barmode='overlay', height=630,
                      xaxis={'title': "Facility", 'titlefont': {'color': 'black', 'size': 24},
                             'tickfont': {'size': 9, 'color': 'black'}},
                      yaxis={'title': "Events", 'titlefont': {'color': 'black', 'size': 24, },
                             'tickfont': {'color': 'black'}})
        },
        style={'width': '1200px',
               'Height': '100px', 'display': 'inline-block'})
])

if __name__ == '__main__':

    app.run_server(debug=True, host='0.0.0.0', port=8050)
