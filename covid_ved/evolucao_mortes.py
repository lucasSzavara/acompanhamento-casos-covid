import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from data import df
from layouts.cards import get_cards

evolucao_mortes = html.Div(get_cards(
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(
                            id='estado-mortes',
                            value=None,
                            options=[{'label': i, 'value': i} for i in df['state'].unique()],
                            placeholder='UF'
                        ),
                        className='col-2'
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='cidade-mortes',
                            value=None,
                            options=[{'label': '', 'value': ''}],
                            placeholder='Cidade'
                        ),
                        className='col-5'
                    )
                ], className='row m-0'
            ),
            html.Div(id='chart_placeholder-mortes', ),
        ],
        id='evolucao_mortes'
    ), header='Evolução de mortes em função do tempo'
), className='col-6')


@app.callback(
    Output('cidade-mortes', 'options'),
    [Input('estado-mortes', 'value')]
)
def buscar_cidades(uf):
    if uf != '':
        cidades_repetidas = df[df['state'] == uf]['city']
        cidades = cidades_repetidas[cidades_repetidas.notnull()].sort_values().unique()
        return [{'label': i, 'value': i} for i in cidades]
    return [{'label': '', 'value': ''}]


@app.callback(
    Output('chart_placeholder-mortes', 'children'),
    [Input('cidade-mortes', 'value'), Input('estado-mortes', 'value')]
)
def gerar_grafico(cidade, uf):
    if cidade is not None and uf is not None:
        df_regiao = df[(df['state'] == uf) & (df['city'] == cidade) & (df['new_confirmed'] >= 0) & (df['is_repeated'] == False)]
        df_regiao.set_index(pd.DatetimeIndex(df_regiao.last_available_date), inplace=True)
        df_regiao = df_regiao.resample('D', origin='start').bfill()
        df_regiao.last_available_date = df_regiao.index.values
    elif uf is not None:
        df_regiao = df[(df['place_type'] == 'state') & (df['state'] == uf) & (df['new_confirmed'] >= 0) & (df['is_repeated'] == False)]
        df_regiao.set_index(pd.DatetimeIndex(df_regiao.last_available_date), inplace=True)
        df_regiao = df_regiao.resample('D', origin='start').bfill()
        df_regiao.last_available_date = df_regiao.index.values
    else:
        df_regiao = df[(df['place_type'] == 'state') & (df['new_confirmed'] >= 0) & (df['is_repeated'] == False)]
        dfs_uf = []
        for uf in df_regiao['state'].unique():
            df_uf = df_regiao[df_regiao['state'] == uf]
            df_uf.set_index(pd.DatetimeIndex(df_uf.last_available_date), inplace=True)
            df_uf = df_uf.resample('D', origin='start').bfill()
            df_uf.last_available_date = df_uf.index.values
            dfs_uf.append(df_uf)

        df_regiao = dfs_uf[0]
        for df_uf in dfs_uf[1:]:
            df_regiao['last_available_deaths'] += df_uf['last_available_deaths']

    fig = go.Figure(go.Scatter(
        x=df_regiao['last_available_date'],
        y=df_regiao['last_available_deaths'],
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
            'title': {'text': 'Total de mortes'},
            'showgrid': True,
            'gridcolor': 'rgba(100, 100, 100, 0.5)',

        },
    )
    return dcc.Graph(id='grafico_evolucao_mortes', figure=fig)
