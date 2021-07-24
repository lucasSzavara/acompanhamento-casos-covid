from data import df
from layouts.cards import get_cards
from layouts.tabela import format_table
import dash_html_components as html
from dash_table.Format import Format, Symbol, Group

df_ultimo_dia = df[
    (df['place_type'] == 'state') &
    (df['is_repeated'] == False)
    ]
df_ultimo_dia = df_ultimo_dia.sort_values(by="last_available_date").drop_duplicates(subset=["state"], keep="last")

series_mortalidade = df_ultimo_dia['last_available_deaths'] / df_ultimo_dia['last_available_confirmed']
df_mortalidade = series_mortalidade.describe().to_frame()
df_mortalidade['Valor'] = df_mortalidade[0] * 100
del df_mortalidade[0]
df_mortalidade = df_mortalidade.reset_index()

titles = {
    'index': 'Estatística'
}

estatisticas = {
    'mean': 'Média',
    '25%': 'Q1',
    '50%': 'Q2',
    '75%': 'Q3'
}

functions_map = {
    'index': lambda x: estatisticas.get(x, x.title())
}

dash_format = {
        'Valor': Format(
            symbol=Symbol.yes,
            symbol_suffix='%',
            group=Group.yes,
            group_delimiter='.',
            decimal_delimiter=','
        ).scheme('f').precision(2)
    }


tabela_estatisticas = html.Div(
    get_cards(
        format_table(
            df_mortalidade[~df_mortalidade['index'].isin(['count', 'std'])],
            titles=titles,
            has_buttons=False,
            functions_map=functions_map,
            dash_format=dash_format
        ),
        header='Estatísticas de taxa de mortalidade por UF'
    ),
    className='col-2'
)
