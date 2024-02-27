# importing required libraries
import datetime
import yfinance as yf
import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output


# importing a external style sheet to help make things look better.
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

# here we are initializing the app dashboard 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)
app.title = "Stock Visualization"

app.layout = html.Div(children=[

#This controls the header of the page. You could connect this to an external css file if you want but to keep
# it simple here though to change a few style settings here.
    html.Div(children=[
        # html.Img(src='cat.png', style={'height': '50px', 'margin-right': '10px'}),
        html.Img(src='./images/cat2.jpg'),
        html.H1("Stonks Dashboard", 
                style={'margin': '15px', 
                       'background-color': 'dogerblue' }),
    ], className='navbar navbar-dark bg-dark'),

# This section controls the input section where we can select a new stock
    html.Div(children=[
        html.H4("Put the name of a stock here if you want to see a pretty graph", 
                style={'margin': '20px'}),
        dcc.Input(id='input', 
                  value='AAPL', 
                  type='text', 
                  style={'margin-left': '20px', 'margin-bottom': '20px'}),

# This is where we are setting up the slider
    dcc.RangeSlider(
        id='year-slider',
        min=2010,
        max=datetime.datetime.now().year,
        step=2,
        # Here we are setting the slider up to go from 2020 to present day. 
        value=[2020, datetime.datetime.now().year],  
        # Is how big of a jump we want to jump on the slider but it makes cense to have it at 1
        marks={year: str(year) for year in range(2010, datetime.datetime.now().year + 1)},
        included=True 
    ),
    ], style={'margin-bottom': '20px'}),

    html.Div(id='output-graph')
])


# callback Decorator: is super important because this is where we connect our data to our graphs
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value'),
     Input(component_id='year-slider', component_property='value')]
)
def update_graph(input_data, selected_years):
    start_year, end_year = selected_years

    start = datetime.datetime(start_year, 1, 1)
    end = datetime.datetime(end_year, 12, 31)

    try:
        df = yf.download(input_data, start=start, end=end)

        # All of the metrics to change the graph
        graph = dcc.Graph(id="example", figure={
            'data': [{'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data}],
            'layout': {
                'title': f"{input_data} Stock Prices ({start_year}-{end_year})",
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Price'},
                'plot_bgcolor': '#f8f9fa',  # background color
                'paper_bgcolor': '#ffffff',  # chart area background color
            }
        })

    except Exception as e:
        graph = html.Div(f"Error retrieving stock data: {str(e)}")

    return graph



if __name__ == '__main__':
    app.run_server(debug=True)
