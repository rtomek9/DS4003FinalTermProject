# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1idghsQnQbgSjhd1RpMUOzc32yoXZVrIn
"""

import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
from datetime import date
import plotly.graph_objects as go
import plotly.io as pio
import base64


#color theme
pio.templates["custom_theme"] = go.layout.Template(
    layout=go.Layout(
        colorway=['#ff0000', '#00ff00', '#0000ff']
    )
)
pio.templates.default = 'custom_theme'
#read data and define for layout
gapminder_df = px.data.gapminder().query("year==2003")
df = pd.read_csv('data/mydata2.csv')
rad_columns = ["stability",	"rights",	"health",	"safety",	"climate",	"cost",	"popularity"]
range = [0,10,20,30,40,50,60,70,80,90,100]

#initialize app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
image_filename = 'ohgraphic.png'
subset_df = df[["country","stability",	"rights",	"health",	"safety",	"climate",	"cost",	"popularity"]]
dropdown_columns = [col for col in df.columns if col not in ['iso_alpha', 'popularity','country']]

#define layout - title, description, dropdowns, radar plot, bar chart, bubble charts, population bubble map
app.layout = html.Div([
        html.Div([
            html.Img(src=app.get_asset_url(image_filename),
                    style={ 'top': 8, 'left': 8, 'width': '12%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'})]),


    html.H2("OH, THE PLACES YOU'LL GO!", style={'text-align': 'center', 'font-family': 'verdana', 'font-weight':' bold'}),
    html.Div([
    html.P("The following dashboard offers an overview of key factors impacting quality of life in 137 different countries across the world. It assesses economic and political stability, legal systems, health services, safety, climate, costs, and popularity. Current data stems from reputable sources such as the World Bank, Transparency.org, the United Nations, and more. Every metric is normalized on a scale from 0-100 based on their source.")
],style={ 'right': 10, 'left': 10}),
        html.Br(),#style={ 'right': 10, 'left': 10})]),
    html.Div([
        html.H4("Select two countries", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in subset_df['country']],
            value=df['country'][12:14],  #pre-select the first two countries
            multi=True  #set multi attribute to True
        ),
       # html.H5("Quality of Life Radar Plot By Countries", style={'text-align': 'center'}),
        dcc.Graph(id='polar-plot', figure={}),
    ], style={'display': 'inline-block', 'width': '50%', 'background-color': '#FD6895', 'border-radius': '20px'}),

    html.Div([
        html.H4("Select two metrics", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': col, 'value': col} for col in dropdown_columns],
            value=["climate", "health"],
            multi=True
        ),
        #html.H5("Bar Plot of Metrics", style={'text-align': 'center'}),
        dcc.Graph(id='bar-chart', figure={}),
    ], style={'display': 'inline-block', 'width': '50%', 'vertical-align': 'top', 'float': 'right', 'background-color': '#FCEB00', 'border-radius': '20px'}),
#'background-color':'#F4EEED', 'border-radius': '20px'
    html.Div([
        html.Div([
            html.Div(id='country-info', style={'text-align': 'center','background-color': '#eeeeee', 'border-radius': '20px'}),
            html.Br(),
            html.H4("Hover over the bubbles to compare all metrics", style={'text-align': 'center', 'background-color': '#FD6895', 'border-radius': '20px', 'padding': 15}),
            html.Div(id='bubble-chart-container', style={'display': 'flex', 'justify-content': 'center'}),

            html.H4("Population by Country", style={'text-align': 'center', 'background-color': '#FD6895', 'padding': 15, 'border-radius': 20}),
            dcc.Graph(id='geo-map', figure={}, style={'align-self': 'center'}),
        ], style={'max-width': '900px', 'margin': '0 auto'}) #style = {'background-color':'#283D3B'}),
    ]),
   html.P("So...be your name Buxbaum or Bixby or Bray"),
   html.P ("or Mordecai Ali Van Allen O'Shea,"),
   html.P("You're off the Great Places!"),
    html.P("Today is your day!"),
html.P("Your mountain is waiting"),
html.P("So...get on your way!"),

html.P("-Dr. Suess", style={'text-align': 'right'}),

])

#callbacks
@app.callback(
    [Output('polar-plot', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_plot(selected_countries, selected_metrics):
#radar
    traces = []
    for country in selected_countries:
        country_data = df[df['country'] == country]
        values = country_data[rad_columns].values.flatten().tolist()
        traces.append(go.Scatterpolar(
            r=values,
            theta=rad_columns,
            fill='toself',
            name=country
        ))
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True
    )
    polar_fig = go.Figure(data=traces, layout=layout)

#bar chart
    bar_traces = []
    for metric in selected_metrics:
        bar_traces.append(go.Bar(
            x=selected_countries,
            y=df[df['country'].isin(selected_countries)][metric],
            name=metric
        ))
    bar_layout = go.Layout(
        barmode='group',
        xaxis=dict(title='Country'),
        yaxis=dict(title='Value')
    )
    bar_fig = go.Figure(data=bar_traces, layout=bar_layout)

    return polar_fig, bar_fig

@app.callback(
    Output('country-info', 'children'),
    [Input('country-dropdown', 'value')] #maybe error
)
def update_country_info(selected_countries):
    info = html.Div(children=[
        html.Div([
            html.H3(country, style={'color': '#FF0000', 'float': 'left', 'width': '100%'}),  #change color to red
            html.P(f"Strength: {df[df['country'] == country][rad_columns].max().idxmax()}"),
            html.P(f"Weakness: {df[df['country'] == country][rad_columns].min().idxmin()}")
        ], style={'margin-bottom': '20px', 'width': '50%', 'float': 'left'})
        if i % 2 == 0 else
        html.Div([
            html.H3(country, style={'color': '#00FF00', 'float': 'right', 'width': '100%'}),  #change color to green
            html.P(f"Strength: {df[df['country'] == country][rad_columns].max().idxmax()}"),
            html.P(f"Weakness: {df[df['country'] == country][rad_columns].min().idxmin()}")
        ], style={'margin-bottom': '20px', 'width': '50%', 'float': 'right'})
        for i, country in enumerate(selected_countries)
    ], style={'width': '100%', 'overflow': 'auto'})

    return info
left_color = '#FF0000'  #red
right_color = '#00FF00'  #green

@app.callback(
    Output('bubble-chart-container', 'children'),
    [Input('country-dropdown', 'value')]
)
def update_bubble_charts(selected_countries):
    bubble_charts = []
    for country in selected_countries:
        #get country info
        country_data = df[df['country'] == country]
        metrics = country_data.columns.drop(['country','population (thousands)','iso_alpha'])

        bubble_fig = go.Figure()

        #iterate over metrics
        for i, metric in enumerate(metrics):
            metric_value = country_data[metric].values[0]
            normalized_value = (metric_value - df[metric].min()) / (df[metric].max() - df[metric].min()) * 100
            color = left_color if i % 2 == 0 else right_color

            bubble_fig.add_trace(go.Scatter(
                x=[country],
                y=[normalized_value],
                mode='markers',
                marker=dict(
                    size=metric_value,
                    color=color,
                    opacity=0.5
                ),
                name=metric
            ))

        bubble_fig.update_layout(
            title=f'{country} Metrics',
            xaxis=dict(title='Country'),
            yaxis=dict(title='Value (normalized)', range=[0, 100]),#set y-axis range from 0 to 100
            showlegend=False
        )
        bubble_charts.append(dcc.Graph(figure=bubble_fig))

    #both bubble charts are returned

    return bubble_charts
left_color = '#FF0000'  #already defined but reference
right_color = '#00FF00'

@app.callback(
    Output('geo-map', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_map(selected_countries):
    if not selected_countries:
        return {}

#filter the data for selected countries by user
    filtered_data = df[df['country'].isin(selected_countries)]

    #bubble map
    fig = px.scatter_geo(filtered_data,
                         locations="iso_alpha",
                         size="population (thousands)",
                         hover_name="country",
                         projection="natural earth")
    if len(selected_countries) >= 1:
        fig.update_traces(marker=dict(color=['#FF0000']))  #first country red
    if len(selected_countries) >= 2:
        fig.update_traces(marker=dict(color=['#00FF00']), selector=dict(name=selected_countries[1]))
    fig.update_layout(
        width=900,
        height=600,
    )
    return fig

if __name__ == '__main__':
    app.run(jupyter_mode='external', debug=True)