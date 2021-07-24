import os

import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from casos_estado import casos_por_estado
from evolucao_cidade import evolucao_cidade
from tabela_resumo import tabela_resumo
from tabela_estatisticas import tabela_estatisticas


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def criar_visualizacao(_):
    return html.Div([
        html.Div(
            [
                evolucao_cidade,
                casos_por_estado
            ],
            className='row m-0'
        ),
        html.Div(
            [
                tabela_resumo,
                tabela_estatisticas
            ],
            className='row m-0'
        )
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
