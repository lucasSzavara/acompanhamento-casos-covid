"""Define funções que constroem cards"""
import dash_html_components as html


def get_cards(content, header=None, border=None, full_height=True, class_name='', content_class_name=''):
    """Cria um card com header.

    Args:
        content: O Conteúdo do card.
        header: O Header do card.
        border: A classe de borda do card.
        full_height: Verdadeiro se o card deve ocupar a altura completa do container pai.
        class_name: As classes CSS adicionais para o card.
        content_class_name: As classes CSS adicionais para o conteúdo do card.
    """
    border = '' if border is None else border
    header = html.Div('') if header is None \
        else html.Div(
        html.H6(header, className='m-0 font-weight-bold text-primary'),
        className='card-header py-3 d-flex flex-row align-items-center justify-content-between'
    )
    return html.Div(
        [
            header,
            html.Div(
                content,
                className=f'card-body pr-1 {"h-100" if full_height else ""} {content_class_name}'
            )
        ],
        className=f'card shadow {border} shadow {class_name} {"h-100" if full_height else ""} p-0 mt-3 mb-3'
    )



