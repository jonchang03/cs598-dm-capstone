import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


### Input Options
# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
# available_indicators = df['Indicator Name'].unique()

# taken from the dataset
unique_zipcodes = ['98118', '98109', '98103', '98112', '98102', '98107', '98105',
                    '98108', '98104', '98122', '98106', '98101', '98134', '98121',
                    '98199', '98146', '98115', '98125', '98119', '98144', '98126',
                    '98116', '98117', '98133', '98136', '98188', '98168', '98178',
                    '98166', '98177']
unique_cuisines = ['Afghan', 'African', 'American (New)', 'American (Traditional)', 'Asian Fusion', 'Australian', 
                    'Barbeque', 'Basque', 'Belgian', 'Brazilian', 'Breakfast & Brunch', 'British', 'Buffets', 
                    'Burgers', 'Cafes', 'Cajun/Creole', 'Cambodian', 'Cantonese', 'Caribbean', 'Cheesesteaks', 
                    'Chicken Wings', 'Chinese', 'Colombian', 'Comfort Food', 'Creperies', 'Cuban', 'Delis', 
                    'Dim Sum', 'Diners', 'Egyptian', 'Ethiopian', 'Fast Food', 'Filipino', 'Fish & Chips', 'Fondue', 
                    'Food Court', 'Food Stands', 'French', 'Gastropubs', 'German', 'Gluten-Free', 'Greek', 'Haitian', 
                    'Halal', 'Hawaiian', 'Himalayan/Nepalese', 'Hot Dogs', 'Hot Pot', 'Indian', 'Indonesian', 'Irish', 
                    'Italian', 'Japanese', 'Korean', 'Kosher', 'Laotian', 'Latin American', 'Lebanese', 'Live/Raw Food', 
                    'Malaysian', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Modern European', 'Mongolian', 'Moroccan', 
                    'Pakistani', 'Persian/Iranian', 'Pizza', 'Polish', 'Puerto Rican', 'Restaurants', 'Russian', 'Salad', 
                    'Salvadoran', 'Sandwiches', 'Scandinavian', 'Scottish', 'Seafood', 'Senegalese', 'Shanghainese', 
                    'Soul Food', 'Soup', 'Southern', 'Spanish', 'Steakhouses', 'Sushi Bars', 'Szechuan', 'Taiwanese', 
                    'Tapas Bars', 'Tapas/Small Plates', 'Tex-Mex', 'Thai', 'Trinidadian', 'Turkish', 'Vegan', 'Vegetarian', 
                    'Venezuelan', 'Vietnamese']

app.layout = html.Div(children=[
    html.H1('Data Hygiene Prediction'), 

    html.Div([
        html.P('Instructions: Please fill out the following inputs to receive a prediction of how likely a restaurant is to pass a hygiene inspection.'),
        html.Br(),
    ]),

    ##### Input Section #####
    html.Div([
        ### Text Input
        html.I("Please enter your review of the restaurant in the text box."),
        html.Br(),
        dcc.Input(
                id="review_text", 
                type="text", 
                placeholder="Please type in your review here.",
                style={'width': '67%', 'height': '100px', 'display': 'inline-block'},
            ),
        html.Br(), html.Br(),

        ### Cuisine Type
        html.I("Please select the relevant cuisine types from the following dropdown."),
        dcc.Dropdown(
                id='cuisine_type',
                options=[{'label': i, 'value': i} for i in unique_cuisines],
                value='Taiwanese',
                style={'width': '50%'},
                searchable=True,
                clearable=True,
                multi=True,
            ),
        html.Br(),
        
        ### Zipcode Input
        html.I("Please select the zipcode from the following dropdown."),
        dcc.Dropdown(
                id='zipcode',
                options=[{'label': i, 'value': i} for i in unique_zipcodes],
                value='98101',
                style={'width': '50%'}
            ),
        html.Br(),

        ### Average Rating Input
        html.I("Please enter your average rating for the restaurant."),
        dcc.RadioItems(
                id='average_rating',
                options=[{'label': i, 'value': i} for i in list(range(1,6))],
                value=3,
                labelStyle={'display': 'inline-block'}
            ),
        html.Br(),
    ]),

    # html.Div(
    # [
    #     html.I("Try typing in input 1 & 2, and observe how debounce is impacting the callbacks. Press Enter and/or Tab key in Input 2 to cancel the delay"),
    #     html.Br(),
    #     dcc.Input(id="input1", type="text", placeholder=""),
    #     dcc.Input(id="input2", type="text", placeholder="", debounce=True),
    # ]),

    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    ##### Output Section #####
    html.Br(), html.Br(),
    html.Div(id="output"),
   
])

@app.callback(
    Output("output", "children"),
    [Input("review_text", "value"), 
     Input("cuisine_type", "value"),
     Input("zipcode", "value"),
     Input("average_rating", "value")],
)
def update_output(review_text, cuisine_type, zipcode, average_rating):
    return u'Text: {} and Cuisine: {} and Zipcode: {} and Average Rating: {}'.format(review_text, cuisine_type, zipcode, average_rating)



if __name__ == '__main__':
    app.run_server(debug=True)