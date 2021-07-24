import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from data import df
from layouts.cards import get_cards

evolucao_cidade = html.Div(get_cards(
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(
                            id='estado',
                            value=None,
                            options=[{'label': i, 'value': i} for i in df['state'].unique()],
                            placeholder='UF'
                        ),
                        className='col-2'
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='cidade',
                            value=None,
                            options=[{'label': '', 'value': ''}],
                            placeholder='Cidade'
                        ),
                        className='col-5'
                    )
                ], className='row m-0'
            ),
            html.Div(id='chart_placeholder', ),
        ],
        id='evolucao_cidade'
    ), header='Evolução por dia'
), className='col-6')


@app.callback(
    Output('cidade', 'options'),
    [Input('estado', 'value')]
)
def buscar_cidades(uf):
    if uf != '':
        cidades_repetidas = df[df['state'] == uf]['city']
        cidades = cidades_repetidas[cidades_repetidas.notnull()].sort_values().unique()
        return [{'label': i, 'value': i} for i in cidades]
    return [{'label': '', 'value': ''}]


@app.callback(
    Output('chart_placeholder', 'children'),
    [Input('cidade', 'value'), Input('estado', 'value')]
)
def gerar_grafico(cidade, uf):
    if cidade is not None and uf is not None:
        df_cidade = df[(df['state'] == uf) & (df['city'] == cidade) & (df['new_confirmed'] >= 0) & (df['is_repeated'] == False)]
        df_cidade.set_index(pd.DatetimeIndex(df_cidade.last_available_date), inplace=True)
        df_cidade = df_cidade.resample('D', origin='start').bfill()
        df_cidade.last_available_date = df_cidade.index.values
    elif uf is not None:
        df_cidade = df[(df['place_type'] == 'state') & (df['state'] == uf) & (df['new_confirmed'] >= 0) & (df['is_repeated'] == False)]
        df_cidade.set_index(pd.DatetimeIndex(df_cidade.last_available_date), inplace=True)
        df_cidade = df_cidade.resample('D', origin='start').bfill()
        df_cidade.last_available_date = df_cidade.index.values
    else:
        df_cidade = df[(df['place_type'] == 'state') & (df['new_confirmed'] >= 0) & (df['is_repeated'] == False)]
        dfs_uf = []
        for uf in df_cidade['state'].unique():
            df_uf = df_cidade[df_cidade['state'] == uf]
            df_uf.set_index(pd.DatetimeIndex(df_uf.last_available_date), inplace=True)
            df_uf = df_uf.resample('D', origin='start').bfill()
            df_uf.last_available_date = df_uf.index.values
            dfs_uf.append(df_uf)

        df_cidade = dfs_uf[0]
        for df_uf in dfs_uf[1:]:
            df_cidade['last_available_confirmed'] += df_uf['last_available_confirmed']

    fig = go.Figure(go.Scatter(
        x=df_cidade['last_available_date'],
        y=df_cidade['last_available_confirmed'],
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
            'title': {'text': 'Total de casos'},
            'showgrid': True,
            'gridcolor': 'rgba(100, 100, 100, 0.5)',

        },
    )
    return dcc.Graph(id='grafico_evolucao_cidade', figure=fig)
