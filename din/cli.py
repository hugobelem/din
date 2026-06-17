import typer

from datetime import date
from din import settings, future as f


app = typer.Typer()

future_app = typer.Typer()
app.add_typer(future_app, name='future')

@future_app.command('add')
def add(
    kind: f.Kind = typer.Option(..., prompt=True),
    issued: str = typer.Option(..., prompt='Issued date (YYYY-MM-DD)'),
    due: str = typer.Option(..., prompt='Due date (YYYY-MM-DD)'),
    status: f.Status = typer.Option(..., prompt=True),
    amount: int = typer.Option(..., prompt=True),
    paid: int = typer.Option(..., prompt=True),
    contact: str = typer.Option(..., prompt=True),
    category: str = typer.Option(..., prompt=True),
    notes: str = typer.Option('', prompt=True),
) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)

        repo.save(
            f.Future(
                kind=kind,
                issued=date.fromisoformat(issued),
                due=date.fromisoformat(due),
                status=status,
                amount=amount,
                paid=paid,
                contact=contact,
                category=category,
                notes=notes,
            )
        )

    typer.echo('Future saved.')

@future_app.command()
def all():
    with settings.Session() as session:
        repo = f.FutureRepository(session)

        futures = repo.all()

        for item in futures:
            typer.echo(item)

def main():
    app()
