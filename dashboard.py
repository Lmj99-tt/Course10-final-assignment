# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update


# Create a dash application
app = JupyterDash(__name__)
# JupyterDash.infer_jupyter_proxy_config()

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv', 
                         encoding = "ISO-8859-1",
                         dtype={'Launch Site': str})

# Application layout
app.layout = html.Div(children=[
                                # TODO1: Add title to the dashboard
    
                                html.H1(children='SpaceX Launch Records Dashboard'),
                                # REVIEW2: Dropdown creation
                                # Create an outer division 
                                html.Div([
                                    html.Div([
                                        # Create an division for adding dropdown helper text for report type
                                        html.Div(
                                            [
                                            html.H2('Report Type:', style={'margin-right': '2em'}),
                                            ]
                                        ),
                                        # TODO2: Add a dropdown
                                        dcc.Dropdown(id='site-dropdown', 
                                                     # Update dropdown values using list comphrehension
                                                     options=[{'label': 'All Sites', 'value': 'ALL'},
                                                              {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                              {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                              {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                              {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},],
                                                     placeholder="Select a Launch Site here",
                                                     searchable=True,
                                                     style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
                                        # Place them next to each other using the division style
                                        ], style={'display':'flex'}), 
                                    ]), 
                                html.Div([ ], id='success-pie-chart'),
                                
                                html.Div([
                                            html.H2('Payload Mass (kg):', style={'margin-right': '2em'}),
                                            ]
                                        ),
                                
                                html.Div([ ], id='payload-slider'),
                                
                                html.Div([ ], id='success-payload-scatter-chart'),
                                ])

# Callback function definition
# TODO4: Add 5 ouput components
@app.callback([Output(component_id='success-pie-chart', component_property='children'),
              Output(component_id='payload-slider', component_property='children'),
              Output(component_id='success-payload-scatter-chart', component_property='children')],
              [Input(component_id='site-dropdown', component_property='value')])
#pie_chart
def get_graph(entered_site):
    
    filtered_df = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
    if entered_site == 'ALL':
        max_payload = spacex_df['Payload Mass (kg)'].max()
        min_payload = spacex_df['Payload Mass (kg)'].min()
        
        fig = px.pie(filtered_df, values='class',  
        names='Launch Site', 
        title='Total Success Launches By Sites')
        
        fig_s = px.scatter(spacex_df, color="Booster Version Category", 
                           x="Payload Mass (kg)", y="class")
        
        return [dcc.Graph(figure=fig),
                dcc.RangeSlider(min=0, max=10000, step=2500,
                                value=[min_payload, max_payload]),
                dcc.Graph(figure=fig_s)]
    else:
        print(entered_site)
        per_filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['class']).count().reset_index()
        max_payload = spacex_df[spacex_df['Launch Site'] == entered_site]['Payload Mass (kg)'].max()
        min_payload = spacex_df[spacex_df['Launch Site'] == entered_site]['Payload Mass (kg)'].min()
        pie_fig = px.pie(per_filtered_df, values='Flight Number', 
        names='class', 
        title='Total Success Launches For Site')
        
        fig_s = px.scatter(spacex_df[spacex_df['Launch Site'] == entered_site], color="Booster Version Category", 
                           x="Payload Mass (kg)", y="class")
        return [dcc.Graph(figure=pie_fig),
                dcc.RangeSlider(min=0, max=10000, step=2500,
                                value=[min_payload, max_payload]),
                dcc.Graph(figure=fig_s)]
    

# Run the app
if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
    app.run_server()