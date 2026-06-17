import typer

from datetime import date
from din import settings, future as f

from rich import box
from rich.console import Console
from rich.table import Table


app = typer.Typer()
console = Console()

future_app = typer.Typer()
app.add_typer(future_app, name='future')

@future_app.command('add')
def add(
    kind: f.Kind = typer.Option('payable', prompt=True),
    issued: str = typer.Option(date.today(), prompt='Issued date (YYYY-MM-DD)'),
    due: str = typer.Option(..., prompt='Due date (YYYY-MM-DD)'),
    amount: int = typer.Option(..., prompt=True),
    category: str = typer.Option(..., prompt=True),
    notes: str = typer.Option(..., prompt=True),
    contact: str = typer.Option(..., prompt=True),
) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)

        repo.save(
            f.Future(
                kind=kind,
                issued=date.fromisoformat(issued),
                due=date.fromisoformat(due),
                status=f.Status.PENDING,
                amount=amount,
                paid=0,
                contact=contact,
                category=category,
                notes=notes,
            )
        )

    typer.echo('\nSaved ;)')

@future_app.command()
def all():
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        futures = repo.all()

    table = Table(title="Futures", box=box.HORIZONTALS)

    table.add_column('ID')
    table.add_column("Kind")
    table.add_column("Status")
    table.add_column("Due")
    table.add_column("Amount", justify="right")
    table.add_column("Contact")
    table.add_column("Category")

    for future in futures:
        table.add_row(
            str(future.id),
            future.kind.value,
            future.status.value,
            str(future.due),
            str(future.amount),
            future.contact or '-',
            future.category or '-',
        )

    console.print(table)

def main():
    app()
