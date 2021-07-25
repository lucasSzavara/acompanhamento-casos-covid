import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

from data import df
from layouts.cards import get_cards

df_cidade = df[(df['place_type'] == 'state') & (df['is_repeated'] == False)]
fig = go.Figure()

for uf in df_cidade['state'].unique():
    df_uf = df_cidade[df_cidade['state'] == uf]
    df_uf.set_index(pd.DatetimeIndex(df_uf.last_available_date), inplace=True)
    df_uf = df_uf.resample('D', origin='start').bfill()
    df_uf.last_available_date = df_uf.index.values
    fig.add_trace(go.Scatter(
        x=df_uf['last_available_date'],
        y=df_uf['last_available_confirmed_per_100k_inhabitants'],
        name=uf
    ))

fig.update_xaxes(
    dtick="M1",
    tickformat="%m/%Y"
)
fig.update_layout(
    plot_bgcolor='white',
    xaxis={
        'title': {'text': 'Data'},
        'showgrid': True,
        'gridcolor': 'rgba(100, 100, 100, 0.5)'
    },
    yaxis={
        'title': {'text': 'Casos por 100 mil habitantes'},
        'showgrid': True,
        'gridcolor': 'rgba(100, 100, 100, 0.5)',

    },
)

evolucao_estado = html.Div(get_cards(
    html.Div(
        [
            html.Div(dcc.Graph(id='grafico_evolucao_cidade', figure=fig))
        ],
        id='evolucao_por_estado'
    ), header='Comparativo por dia'
), className='col-6')
