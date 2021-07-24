"""Define uma função para criar uma tabela"""
import dash_table
import pandas as pd


def format_table(
        df: pd.DataFrame,
        functions_map=None,
        titles=None,
        remove=None,
        column_widths=None,
        dash_format=None,
        presentation=None,
        has_buttons=True,
):
    if column_widths is None:
        column_widths = []
    if functions_map is None:
        functions_map = {}
    if titles is None:
        titles = {}
    if remove is None:
        remove = []
    if presentation is None:
        presentation = {}
    if dash_format is None:
        dash_format = {}

    for i, value in functions_map.items():
        try:
            df[i] = df[i].apply(value)
        except:
            print(i)

    columns = [
        {
            "name": titles.get(i, ' '.join(str(i).title().split('_'))),
            "id": i,
            "hideable": has_buttons,
            'type': 'numeric',
            "format": dash_format.get(i),
            "presentation": presentation.get(i, 'input')
        } for i in df.columns
    ]
    for col in remove:
        try:
            del df[col]
        except:
            print(f'Coluna {col} não existe')
    return dash_table.DataTable(
        id="dash",
        columns=columns,
        data=df.to_dict("records"),
        sort_action="native",
        filter_action="native",
        style_data_conditional=[
                                   {"if": {"row_index": "odd"}, "backgroundColor": "#ddf2f0"}, ] + [
                                   {'if': {'column_id': i}, 'minWidth': j} for i, j in column_widths],
        style_cell={
            "textAlign": "left",
            'color': 'black',
            'padding': '0 10px',
            'minWidth': '130px'
        },
        style_header={"backgroundColor": "#17a2b8", "color": "white"},
        export_format="xlsx" if has_buttons else None,
        page_size=10,
        style_table={'overflowX': 'auto'},
    )
