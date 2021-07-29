import db
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

from datetime import date
# -*- coding: utf-8 -*-

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])


app.layout  = title_card = dbc.Card(
    [
        dbc.CardBody(
            [

                html.H1("Test Deployment - VAP", className="card-title"),

                ], style = {'text-align': 'center'} ),


    ]
)


table_framing = dbc.Card([
        dbc.CardBody(
            [html.P("Consumption per Space",style={'text-align':'center'}),


        dash_table.DataTable(
        id='framing_table',
        columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in db.df_sections.columns],
        data=db.df_sections.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 11,
        style_table={'overflowY': 'scroll'},
        #style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        #style_cell={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'}
        #fixed_rows={'headers': True},
        style_cell={'minWidth': 99, 'width': 99, 'maxWidth': 99}

        ),
                ])
]),

pie_framing = dbc.Card(
    [
        dbc.CardBody(
            [

                html.P(""),
                html.Div(id='pie_framing')


 ],)]),


table_framing_comparisson = dbc.Card([
        dbc.CardBody(
            [html.P("Robot & Revit Section Comparisson",style={'text-align':'center'}),


        dash_table.DataTable(
        id='framing_comparisson',
        columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in db.df_section_comprisson.columns],
        data=db.df_section_comprisson.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 11,
        style_table={'overflowY': 'scroll'},
        #style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        #style_cell={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'}
        #fixed_rows={'headers': True},
        style_cell={'minWidth': 99, 'width': 99, 'maxWidth': 99}

        ),
                ])
]),





app.layout = html.Div([
    dbc.Row([dbc.Col(title_card, width=12)],justify="center"),
    dbc.Row([dbc.Col(html.P(""))]),
    dbc.Row([dbc.Col(table_framing, width=6),dbc.Col(pie_framing, width=6)],style={}),
    dbc.Row([dbc.Col(table_framing_comparisson, width=8)], style={}),
])



@app.callback(
    Output('framing_table', 'style_data_conditional'),
    [Input('framing_table', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]
    print(i)







@app.callback(
    Output('pie_framing', "children"),
    [Input('framing_table', "derived_virtual_data"),
     Input('framing_table', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    df_temp = db.df_sections if rows is None else pd.DataFrame(rows)
    #df_temp = df_temp.groupby(["space_type_el"]).sum()

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#9cd900'
                    for i in range(len(df_temp))],



    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        'labels':df_temp["Type"],"values":df_temp["Volume"], 'type': 'pie',
                        'hoverinfo': "Type",
                    }
                ],
                "layout": {
                    'title': {'text': "Profile Distribution by Volume "},
                    #"barmode": "stack",
                    #"plot_bgcolor":colors,
                    "xaxis": {"automargin": True},
                    "yaxis": { "automargin": True, "title": {"text": "Volume"}},
                    #"color": "rgb(0,0,255)",
                    "height": 450,
                    #"marker":{"line":{"color":"#9cd900", "colorscale":"[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]"}},
                    "autocolorscale":"True",
                    "text": "aaaa",
                    # "margin": {"t": 10, "l": 10, "r": 10},
                    "showlegend": True,

                    #"textposition": 'outside',
                    #'textinfo': "",
                    #'hovertext': "",
                    #'hoverinfo': ""
                    },
                "marker": {'symbol': 'diamond-open', 'size': 15}
                # 'paper_bgcolor': "#303030"
                ,
            },
        )

        for column in ["Type"] if column in df_temp
    ]



if __name__ == '__main__':


  app.run_server()