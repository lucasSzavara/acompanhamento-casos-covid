from data import df
from layouts.cards import get_cards
from layouts.tabela import format_table
import dash_html_components as html
from dash_table.Format import Format, Symbol, Group

df_ultimo_dia = df[
    (df['place_type'] == 'state') &
    (df['new_confirmed'] >= 0) &
    (df['is_repeated'] == False) &
    (df['last_available_date'] == df['last_available_date'].max())
    ]

df_ultimo_dia['last_available_death_rate'] = df_ultimo_dia['last_available_death_rate'] * 100

titles = {
    'state': 'UF',
    'last_available_confirmed': 'Casos confirmados',
    'last_available_deaths': 'Mortes confirmadas',
    'estimated_population': 'População em 2020',
    'last_available_confirmed_per_100k_inhabitants': 'Casos confirmados por 100 mil habitantes',
    'last_available_death_rate': 'Taxa de mortalidade',
}

dash_format = {
        'estimated_population': Format(
            group=Group.yes,
            group_delimiter='.',
        ).scheme('d'),
        'last_available_confirmed': Format(
            group=Group.yes,
            group_delimiter='.',
        ).scheme('d'),
        'last_available_deaths': Format(
            group=Group.yes,
            group_delimiter='.',
        ).scheme('d'),
        'last_available_confirmed_per_100k_inhabitants': Format(
            group=Group.yes,
            group_delimiter='.',
            decimal_delimiter=','
        ).scheme('f').precision(2),
        'last_available_death_rate': Format(
            symbol=Symbol.yes,
            symbol_suffix='%',
            group=Group.yes,
            group_delimiter='.',
            decimal_delimiter=','
        ).scheme('f').precision(2)
    }

tabela_resumo = html.Div(
    get_cards(
        format_table(
            df_ultimo_dia[[
                'state',
                'estimated_population',
                'last_available_confirmed',
                'last_available_deaths',
                'last_available_confirmed_per_100k_inhabitants',
                'last_available_death_rate',
            ]],
            titles=titles,
            dash_format=dash_format
        ),
        header='Resumo'
    ),
    className='col-10'
)
