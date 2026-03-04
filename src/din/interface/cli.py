import typer
from . import transaction_app, balance_app, income_app, expense_app, total_app


app = typer.Typer(no_args_is_help=True)
app.add_typer(transaction_app, name='t')
app.add_typer(balance_app, name='balance')
app.add_typer(income_app, name='income')
app.add_typer(expense_app, name='expense')
app.add_typer(total_app, name='total')
