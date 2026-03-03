import typer
from . import transaction, balance, income, expense


app = typer.Typer(no_args_is_help=True)
app.add_typer(transaction, name='t')
app.add_typer(balance, name='balance')
app.add_typer(income, name='income')
app.add_typer(expense, name='expense')
