#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Add title to the dashboard
    html.H1("Automobile Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': 20}
        )
    ]),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=None,
            placeholder='Select Year',
            style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': 20}
        )
    ]),

    # TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

# TASK 2.4: Creating Callbacks
# Enable or disable the year dropdown based on selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # enable dropdown
    else:
        return True   # disable dropdown

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # TASK 2.5: Create and display graphs for Recession Report Statistics

        # Plot 1
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                            title="Average Automobile Sales fluctuation over Recession Period"))

        # Plot 2
        average_sales = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Year', y='Automobile_Sales', color='Vehicle_Type',
                                           title='Average Automobile Sales by Vehicle Type over Recession Period'))

        # Plot 3
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                                           title='Total Advertising Expenditure Share by Vehicle Type during Recessions'))

        # Plot 4
        unemp_rate = recession_data.groupby(['Vehicle_Type'])[['Automobile_Sales', 'unemployment_rate']].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_rate, x='Vehicle_Type', y='Automobile_Sales',
                                           color='unemployment_rate',
                                           labels={'unemployment_rate': 'Unemployment Rate'},
                                           title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [html.Div(children=[
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([], style={'height': '20px'}),  # space between rows
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})])]

    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # TASK 2.6: Create and display graphs for Yearly Report Statistics

        # Plot 1
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                            title='Total Yearly Automobile Sales'))

        # Plot 2
        mas = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                            title='Total Monthly Automobile Sales'))

        # Plot 3
        avr_vdata = yearly_data.groupby(['Month', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Month', y='Automobile_Sales', color='Vehicle_Type',
                                           title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}'))

        # Plot 4
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                                           title=f'Total Advertisement Expenditure for each Vehicle Type in the year {input_year}'))

        return [html.Div(children=[
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([], style={'height': '20px'}),  # space between rows
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})])]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)

#In the console run
# !pip install setuptools
# !pip install packaging
# !pip install pandas dash
# !pip install more-itertools
# %run Dashboard_for_yearwise_and_recessionwise_trend.py