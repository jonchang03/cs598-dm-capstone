import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
from joblib import dump, load

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # the Flask app

### Load input options and model
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
# load serialized model
serialize_path = './pipeline.joblib'
pipeline_serialized = load(serialize_path) 

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
        dcc.Textarea(
                id="review_text", 
                placeholder="Please type in your review here.",
                value="Please type in your review here.",
                style={'width': '67%', 'height': '100px'},
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
                options=[{'label': i, 'value': i} for i in ['1', '2', '3', '4', '5']],
                value='3',
                labelStyle={'display': 'inline-block'}
            ),
        html.Br(),
    ]),

    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    ##### Output Section #####
    html.Br(), html.Br(),
    html.Div(id="output"),
   
])

@app.callback(
    Output("output", "children"),
    [Input("submit-button", "n_clicks")], 
     state=[State("review_text", "value"), 
            State("cuisine_type", "value"),
            State("zipcode", "value"),
            State("average_rating", "value")],
)
def update_output(n_clicks, review_text, cuisine_type, zipcode, average_rating):
    cuisine_type = str(cuisine_type) # need to convert list to string
    data = [[review_text, cuisine_type, zipcode, average_rating]]
    input_df = pd.DataFrame(data, columns = ['text', 'cuisines_offered', 'zipcode', 'avg_rating'])
    pred = float(pipeline_serialized.predict_proba(input_df)[:,1])
    output_string = 'This restaurant is: {:.2%} likely to pass a hygiene inspection'.format(pred)
    return output_string


if __name__ == '__main__':
    app.run_server(debug=True)