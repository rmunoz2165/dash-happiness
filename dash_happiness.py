import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

happiness = pd.read_csv('../data/world_happiness.csv')

region_options = [{'label': i,  'value': i} for i in happiness['region'].unique()]
country_options = [{'label': i,  'value': i} for i in happiness['country'].unique()]
data_options = [{'label': 'Happiness Score', 'value': 'happiness_score'},
                {'label': 'Happiness Rank', 'value': 'happiness_rank'}]


line_fig = px.line(happiness[happiness['country'] == 'United States'],
                   x='year',  y='happiness_score',
                   title='Happiness Score in the USA')

app = dash.Dash()

app.layout = html.Div([
    html.H1('World Happiness Dashboard'),
    html.P(['This dashboard shows the happiness score.',
            html.Br(),
            html.A('World Happiness Report Data Source',
                   href='https://worldhappiness.report/',
                   target='_blank')]),
    dcc.Dropdown(id='country-dropdown',
                 options=country_options,
                 value='United States'),
    dcc.RadioItems(id='data-radio',
                   options=data_options,
                   value='happiness_score'),
    dcc.Graph(id='happiness-graph'),
    html.Div(id='average-div')])

@app.callback(
    Output(component_id='happiness-graph', component_property='figure'),
    Output('average-div', 'children'),
    Input(component_id='country-dropdown', component_property='value'),
    Input('data-radio', 'value')
)
def update_graph(selected_country, selected_data):
    filtered_happiness = happiness[happiness['country'] == selected_country]
    line_fig = px.line(filtered_happiness,
                       x='year', y= selected_data,
                       title=f'{selected_data} in {selected_country}')
    selected_avg=filtered_happiness[selected_data].mean()
    return line_fig, f'The average {selected_data} for {selected_country} is '\
                    f'{round((selected_avg),2)}'


if __name__ == "__main__":
    app.run_server(debug=True)
