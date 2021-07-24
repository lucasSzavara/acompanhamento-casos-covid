import dash
import dash_core_components as dcc
import dash_html_components as html


# Importar Bootstrap
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'crossorigin': 'anonymous'
    },
]

# Criar instância da aplicação
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

# Criar layout inicial
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(html.Div('', id='loading'), id='page-content'),
    ],
    id='content'
)
