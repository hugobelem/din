import typer
from . import transaction, balance


app = typer.Typer(no_args_is_help=True)
app.add_typer(transaction, name='t')
app.add_typer(balance, name='balance')
