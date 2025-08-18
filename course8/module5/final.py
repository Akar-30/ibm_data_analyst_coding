import os
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt


#Create app
app = dash.Dash(__name__)
#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True
# Read the wildfire data into pandas dataframe

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'historical_automobile_sales.csv')
df = pd.read_csv(csv_path)


app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select Statistics',
            value='Select Statistics',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 10px'}),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in range(1980, 2024)],
            placeholder='Select year',
            value=None,
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'},
            disabled=True
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 10px'}),
    html.Br(),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-direction': 'column'}),
    ])
])


def compute_graphes_for_yearly_statistics(input_year):
    
    # Filter data for the selected year
    yearly_data = df[df['Year'] == input_year]
                          
    # Plot 1: Yearly Automobile sales using line chart for the whole period.
    # grouping data for plotting.
    # Hint:Use the columns Year and Automobile_Sales.
    yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
    Y_chart1 = dcc.Graph(figure=px.line(yas, 
        x='Year',
        y='Automobile_Sales',
        title='Yearly Automobile Sales'))
        
    # Plot 2: Total Monthly Automobile sales using line chart.
    # grouping data for plotting.
    # Hint:Use the columns Month and Automobile_Sales.
    mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
    Y_chart2 = dcc.Graph(figure=px.line(mas,
        x='Month',
        y='Automobile_Sales',
        title='Total Monthly Automobile Sales'))

    # Plot bar chart for average number of vehicles sold during the given year
    # grouping data for plotting.
    # Hint:Use the columns Year and Automobile_Sales
    avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
        x='Vehicle_Type',
        y='Automobile_Sales',
        title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

    # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
    # grouping data for plotting.
    # Hint:Use the columns Vehicle_Type and Advertising_Expenditure
    exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    Y_chart4 = dcc.Graph(
        figure=px.pie(exp_data, 
        values='Advertising_Expenditure',
        names='Vehicle_Type',
        title='Total Advertisment Expenditure for Each Vehicle'))
        
    return [
        html.Div(className='chart-item', children=[html.Div(children=Y_chart1, style={'width': '50%'}),html.Div(children=Y_chart2, style={'width': '50%'})],style={'display':'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=Y_chart3, style={'width': '50%'}),html.Div(children=Y_chart4, style={'width': '50%'})],style={'display': 'flex'})
    ]



def compute_graphes_for_recession_statistics():

    
    recession_data = df[df['Recession'] == 1]

    # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
    # grouping data for plotting
    yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    # Plotting the line graph
    R_chart1 = dcc.Graph(
        figure=px.line(yearly_rec, 
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales fluctuation over Recession Period"))

    # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
    # use groupby to create relevant data for plotting. 
    # Hint:Use Vehicle_Type and Automobile_Sales columns
    average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                
    R_chart2 = dcc.Graph(
        figure=px.bar(average_sales,
        x='Vehicle_Type',
        y='Automobile_Sales',
        title="Average Vehicles Sold by Vehicle Type during Recession"))

    # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
    # grouping data for plotting
    # Hint:Use Vehicle_Type and Advertising_Expenditure columns
    exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    R_chart3 = dcc.Graph(
        figure=px.pie(exp_rec,
        values='Advertising_Expenditure',
        names='Vehicle_Type',
        title="Total Expenditure Share by Vehicle Type during Recessions"))

    # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
    # grouping data for plotting
    # Hint:Use unemployment_rate,Vehicle_Type and Automobile_Sales columns
    unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
    R_chart4 = dcc.Graph(figure=px.bar(unemp_data,
    x='unemployment_rate',
    y='Automobile_Sales',
    color='Vehicle_Type',
    labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
    title='Effect of Unemployment Rate on Vehicle Type and Sales'))

    return [
        html.Div(className='chart-item', children=[html.Div(children=R_chart1, style={'width': '50%'}), html.Div(children=R_chart2, style={'width': '50%'})], style={'display': 'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=R_chart3, style={'width': '50%'}), html.Div(children=R_chart4, style={'width': '50%'})], style={'display': 'flex'})
    ]


# Update Input Container callback function
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True


# Update Output Container callback function
@app.callback(Output(component_id='output-container', component_property='children'),
               [Input(component_id='dropdown-statistics', component_property='value'), 
                Input(component_id='select-year', component_property='value')]
               )

def update_output_container(selected_statistics, input_year):  
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        return compute_graphes_for_recession_statistics()
    elif selected_statistics == 'Yearly Statistics':  
        return compute_graphes_for_yearly_statistics(input_year)


if __name__ == '__main__':
    app.run()
    