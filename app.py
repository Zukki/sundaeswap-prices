import pandas as pd
from datetime import datetime
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

url='https://drive.google.com/file/d/1QaMrBMoczpE5jCoklq11oVIZIf8LRKQ1/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url)

print(df.head(1))
print(df.tail(1))
print(df.info())

df['DateTime'] = pd.to_datetime(df['DateTime'])

FILTER_DATE = datetime.fromisoformat('2022-02-13 19:00:00')

pairs = df['_PAIR_ID'].unique()
pairDefault = 'SUNDAE/ADA_0.3'
pairOptions = []
for pair in pairs:
    item = {"label": pair, "value": pair}
    pairOptions.append(item)

app = Dash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    html.H2("SundaeSwap prices", style={'text-align': 'center'}),
    
    html.Label("Select Pair (Pair_LP Fee %)"),
    dcc.Dropdown(id="slct_pair",
                 options=pairOptions,
                 multi=False,
                 value=pairDefault,
                 style={'width': "40%"}
                 ),
    
    html.Br(),
    
    html.Label("Select foo"),
    dcc.Dropdown(id="slct_date",
                 options=[],
                 multi=False,
                 #value=pairDefault,
                 style={'width': "40%"}
                 ),
    
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_pair', component_property='value'),
     Input(component_id='slct_date', component_property='value'),]
)
def update_graph(slcted_pair, slcted_date):
    print(slcted_pair)
    print(type(slcted_pair))
    print(slcted_date)
    print(type(slcted_date))

    
    filter = (df['DateTime'] > FILTER_DATE) & (df['_PAIR_ID'] == slcted_pair)
    filteredDf = df[filter].copy()
        
    container = "Filtering by: {0}, {1} | {2}".format(slcted_pair, slcted_date, filteredDf.shape)

    # Plotly Express
    # https://plotly.com/python-api-reference/generated/plotly.express.bar.html#plotly.express.bar
    fig = px.line(
        x = 'DateTime',
        y = 'PairPrice',
        data_frame= filteredDf,
        #range_y = [0, 100]
    )

    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)