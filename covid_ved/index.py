import os

import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from casos_estado import casos_por_estado
from mortes_estado import mortes_por_estado
from evolucao_casos import evolucao_casos
from evolucao_mortes import evolucao_mortes
from tabela_resumo import tabela_resumo
from tabela_estatisticas import tabela_estatisticas
from comparacao_casos_por_estado import evolucao_estado
from comparacao_mortalidade_por_estado import evolucao_mortalidade


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def criar_visualizacao(_):
    return html.Div([
        html.Div(
            [
                evolucao_casos,
                evolucao_mortes
            ],
            className='row m-0'
        ),
        html.Div(
            [
                tabela_resumo,
                tabela_estatisticas
            ],
            className='row m-0 mt-3'
        ),
        html.Div(
            [
                evolucao_estado,
                evolucao_mortalidade
            ],
            className='row m-0 mt-3'
        ),
        html.Div(
            [
                casos_por_estado,
                mortes_por_estado
            ],
            className='row m-0 mt-3'
        ),
    ])


server = app.server

if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 8052
    app.run_server(debug=True, host=host, port=port)
