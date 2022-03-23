import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

# Reading covid-19 dataset .csv file using panda
covid_data_frame = pd.read_csv('assets/data/covid_19_data_tr.csv')

# Reading covid-19 dataset vaccination .csv file using panda
vaccine_data_frame = pd.read_csv('assets/data/turkey_vaccine.csv', sep=";")

# Setting each data frame value to its column
daily_first_dose_vaccinations = vaccine_data_frame[['daily_first_dose_vaccinations']].iloc[-1:]
daily_second_dose_vaccinations = vaccine_data_frame[['daily_second_dose_vaccinations']].iloc[-1:]

# Setting each data frame value to its column
conf_cases = covid_data_frame[['Confirmed']]
recv_cases = covid_data_frame[['Recovered']]
dead_cases = covid_data_frame[['Deaths']]

# Adds all values from a certain data frame (ex. confirmed)
def get_total_value(data):
    return ("{:,}".format(int(data.sum())))

# Function to get category and make a graph with its value
def get_category(category_value):
    fig = px.line(covid_data_frame, x="Last_Update", y=category_value)
    fig.update_layout(title_x=0.5, plot_bgcolor= "#D1D6DA", paper_bgcolor="white", xaxis_title="Date", yaxis_title="Cases")
    return fig

# Setting total conf,recv,dead,1st and 2nd vaccinations to variables
total_conf_cases = get_total_value(conf_cases)
total_recv_cases = get_total_value(recv_cases)
total_dead_cases = get_total_value(dead_cases)
total_first_dose_vaccinations= get_total_value(daily_first_dose_vaccinations)
total_second_dose_vaccinations= get_total_value(daily_second_dose_vaccinations)


# Template for the information cards
def card_template(card_header, card_value, card_category):
    card_head_style = {'textAlign':'center', 'fontSize': '150%', 'color':'white'}
    card_body_style = {'textAlign':'center', 'fontSize': '200%', 'color':'white'}
    card_header = dbc.CardHeader(
        [
            html.I(className="bi bi-info-circle-fill me-2"),
            card_header
        ], style=card_head_style
    )
    card_body = dbc.CardBody(
        [
            html.H5(f"{card_value}", className="card-title", style=card_body_style),
            html.P( card_category, className="card-text", style={'textAlign': 'center'}),
        ], style={'color':'white'}
    )
    card = [card_header, card_body]
    return card

# External JavaScript files
external_scripts = [
    'https://platform.twitter.com/widgets.js',
    {'src': 'https://platform.twitter.com/widgets.js'},
    {
        'src': 'https://platform.twitter.com/widgets.js',
        'async': '',
        'charset':'utf-8'
    }
]
# Start Dash Application
app = dash.Dash(__name__,external_scripts=external_scripts, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
app.title = ("Covid19 Dashboard")

# Start webpage Layout
app.layout = html.Div([
        dbc.Container([

        dbc.Row([
            # old color: #34495E
            html.H1("🇹🇷 Covid 19 Dashboard", style={'textAlign':'center', 'color':'white'}),

        ]),
        dbc.Row([
            html.Br()
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(card_template("Confirmed", total_conf_cases, "Total Confirmed Cases",), color="warning")),
            dbc.Col(dbc.Card(card_template("Recovered", total_recv_cases, "Total Recovered Cases"), color="success")),
            dbc.Col(dbc.Card(card_template("Deaths", total_dead_cases, "Total Death Cases"), color="danger")),
            dbc.Col(dbc.Card(card_template("1st Vaccination", total_first_dose_vaccinations, "Total Vaccinated 1st Dose"), color="secondary")),
            dbc.Col(dbc.Card(card_template("2nd Vaccination", total_second_dose_vaccinations, "Total Vaccinated 2nd Dose"), color="info")),

        ], style={'textAlign':'center'}),


dbc.Row([
    dbc.Row([
        html.Br()
    ]),
    dbc.Col(
        dcc.Dropdown(id='category_dropdown', options=[{'label': 'Confirmed', 'value': 'Confirmed'},{'label': 'Recovered', 'value': 'Recovered'},{'label': 'Deaths', 'value': 'Deaths'}], value=["Recovered"],multi=True), md=dict(size=5), className='inline')]),
        html.P("* Select Items that you want to show in the graph", className="card-text", style={'color':'white'}),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id="covid_graph", figure=get_category('Recovered')), md=dict(size=7, offset=0), className='mb-4'),
        dbc.Col(html.A("Tweets by saglikbakanligi", className="twitter-timeline", href="https://twitter.com/saglikbakanligi?ref_src=twsrc%5Etfw"), md=dict(size=5, offset=0), className='mb-4')
    ]),
], className="bg-dark rounded-3")
], className="bg-dark")

# Callback resposible for dynamic graph using the dropdown with ID (category_dropdown)
@app.callback(
    Output('covid_graph', 'figure'),
    Input('category_dropdown', 'value')
)

# update display using information from the the get_category function with the input value
def update_output_display(input_value):
    return get_category(input_value)

# Run Server
if __name__ == '__main__':
    app.run_server(debug=True)

