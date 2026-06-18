import typer

from datetime import date
from calendar import monthrange

from din import settings, future as f

from rich import box
from rich.console import Console
from rich.table import Table


app = typer.Typer()
console = Console()

future_app = typer.Typer()
app.add_typer(future_app, name='future')

@future_app.command()
def add(
    kind: f.Kind = typer.Option('payable', prompt=True),
    issued: str = typer.Option(date.today(), prompt='Issued date (YYYY-MM-DD)'),
    due: str = typer.Option(..., prompt='Due date (YYYY-MM-DD)'),
    amount: int = typer.Option(..., prompt=True),
    category: str = typer.Option(..., prompt=True),
    notes: str = typer.Option(..., prompt=True),
    contact: str = typer.Option(..., prompt=True),
    recurrence: f.Recurrence = typer.Option('once', prompt=True),
) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)

        due_date = date.fromisoformat(due)

        future = f.Future(
            kind=kind,
            issued=date.fromisoformat(issued),
            due=due_date,
            status=f.Status.PENDING,
            amount=amount,
            paid=0,
            recurrence=recurrence,
            contact=contact,
            category=category,
            notes=notes,
        )

        if recurrence == f.Recurrence.ONCE:
            repo.save(future)

        elif recurrence == f.Recurrence.MONTHLY:
            while True:
                try:
                    due_day = int(input('Due day (1-31): '))
                    if due_day > 0 and due_day < 32:
                        break
                except ValueError:
                    typer.echo('Choose a number between 1 and 31')


            year = due_date.year
            month = due_date.month
            original_day = due_day

            ramaining_months = 12 - month or 1

            for _ in range(ramaining_months + 1):
                if month > 12: break
                
                last_day = monthrange(year, month)[1]
                due_day = min(original_day, last_day)

                future.due = date(year, month, due_day)
                repo.save(future)

                month += 1

        elif recurrence == f.Recurrence.INSTALLMENTS:
            installments = 0
            try:
                installments = int(input('Installments number: '))
            except ValueError:
                typer.echo('Choose a valid number')

            while True:
                try:
                    due_day = int(input('Due day (1-31): '))
                    if due_day > 0 and due_day < 32:
                        break
                except ValueError:
                    typer.echo('Choose a number between 1 and 31')

            year = due_date.year
            month = due_date.month
            original_day = due_day
            count = 1
            notes = f'{future.notes}'
        
            for _ in range(installments):
                last_day = monthrange(year, month)[1]
                due_day = min(original_day, last_day)

                future.due = date(year, month, due_day)
                future.notes = f'{notes} [{count}/{installments}]'
                repo.save(future)

                count += 1
                month += 1
                if month > 12:
                    year += 1
                    month = 1

    typer.echo('\nSaved ;)')

@future_app.command()
def all():
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        futures = repo.all()

    table = Table(title="Futures", box=box.SIMPLE)

    table.add_column("ID")
    table.add_column("Kind")
    table.add_column("Status")
    table.add_column("Contact")
    table.add_column("Amount", justify="right")
    table.add_column("Paid", justify="right")
    table.add_column("Due")
    table.add_column("Recurrence")
    table.add_column("Category")
    table.add_column("notes")

    for future in futures:
        table.add_row(
            str(future.id),
            future.kind.value,
            future.status.value,
            future.contact or '-',
            str(f'{future.amount / 100 :.2f}'),
            str(f'{future.paid / 100 :.2f}'),
            str(future.due),
            future.recurrence.value,
            future.category or '-',
            future.notes or '-'
        )

    console.print(table)

@future_app.command('del')
def delete(id: str):
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        is_deleted = repo.delete(id)

    if is_deleted:
        typer.echo('\nDeleted ;)')
    else:
        typer.echo('\nFuture not found :(')

def main():
    app()
