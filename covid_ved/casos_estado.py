import json

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from data import df
from layouts.cards import get_cards

with open('./datasets/brazil_geo.json') as response:
    ufs = json.load(response)

uf_df = df[(df['is_last']) & (df['place_type'] == 'state')]

fig = go.Figure(go.Choropleth(
    locationmode='geojson-id',
    geojson=ufs,
    locations=uf_df['state'],
    z=uf_df['last_available_confirmed_per_100k_inhabitants'],
    colorbar={
        'thicknessmode': 'fraction',
        'thickness': 0.025,

    }
))
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title_text='Casos confirmados por 100 mil habitantes',
    margin={'r': 0, 'l': 0, 't': 0, 'b': 0},
    height=500,
)

casos_por_estado = html.Div(get_cards(
    html.Div(
        [
            dcc.Graph(
                id='casos_estado',
                figure=fig
            )
        ],
        id='casos_por_estado'
    ),
    header='Casos por estado por 100 mil habitantes',
), className='col-6')
