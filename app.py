import pandas as pd
from datetime import datetime
import plotly.express as px  # (version 4.7.0 or higher)
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import requests
import json


FILTER_DATE = datetime.fromisoformat('2022-02-13 19:00:00')

pairDefault = 'SUNDAE/ADA_0.3'
pairOptions = [{"label": 'SUNDAE/ADA_0.3', "value": 'SUNDAE/ADA_0.3'},
               {"label": 'WMT/ADA_0.3', "value": 'WMT/ADA_0.3'},
               {"label": 'LQ/ADA_0.3', "value": 'LQ/ADA_0.3'},
               {"label": 'MIN/ADA_0.3', "value": 'MIN/ADA_0.3'},
               {"label": 'MELD/ADA_0.3', "value": 'MELD/ADA_0.3'},
               {"label": 'MILK/ADA_0.3', "value": 'MILK/ADA_0.3'}]
# pairOptions = []
# try:
#     pairs = df['PairId'].unique()
#     for pair in pairs:
#         item = {"label": pair, "value": pair}
#         pairOptions.append(item)
# except:
#     print('PairId error')
    
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

    df = getDF(slcted_pair)
    
    filter = (df['DateTime'] > FILTER_DATE) & (df['PairId'] == slcted_pair)
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
def getDF(asset):
    jData = getFromApi(asset)

    df = pd.DataFrame(jData, columns =['PairId','Index','DateTimeUnix','PairPrice'])
    df = df.set_index('Index')

    def datetimeFromUnix(ts:str):
        return datetime.utcfromtimestamp(int(ts))

    df['PairPrice'] = df['PairPrice'].astype(float)
    df['DateTime'] = df['DateTimeUnix'].apply(datetimeFromUnix)
    df.info()

    #### END -- DF FROM API ##########################################################

    print(df.head(1))
    print(df.tail(1))
    print(df.info())
    
    return df

def getFromApi(asset):
    #### DF FROM API ##########################################################
    #url = "https://601fa5cgn2.execute-api.us-east-1.amazonaws.com/Dev/assets?asset=SUNDAE/ADA_0.3"
    url = "https://601fa5cgn2.execute-api.us-east-1.amazonaws.com/Dev/assets?asset="+asset
    myResponse = requests.get(url)
    print (myResponse.status_code)
    jData = {}
    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
        print("The response contains {0} properties".format(len(jData)))
    else:
    # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()
    
    return jData









# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)