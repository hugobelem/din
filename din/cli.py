import typer

from datetime import date
from calendar import monthrange

from din import settings, future as f

from rich import box
from rich.console import Console, Group
from rich.table import Table
from rich.align import Align


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
def update(
    id: str,
    status: f.Status | None = typer.Option(None),
    contact: str | None = typer.Option(None),
    amount: int | None = typer.Option(None),
    paid: int | None = typer.Option(None),
    category: str | None = typer.Option(None),
    notes: str | None = typer.Option(None),
    due: str | None = typer.Option(None),
    ) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        future = repo.get(id)
        
        if not future:
            typer.echo('\nFuture not found :(')
            return
        
        if not any([status, contact, amount, paid, category, notes, due]):
            typer.echo('Inform a field to be updated.')

        if status is not None:
            future.status = status

        if contact is not None:
            future.contact = contact

        if amount is not None:
            future.amount = amount

        if paid is not None:
            future.paid = paid

        if due is not None:
            future.due = date.fromisoformat(due)

        if category is not None:
            future.category = category

        if notes is not None:
            future.notes = notes

        repo.update(future)

@future_app.command()
def all() -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        futures = repo.all()

    table = Table(title='Futures', box=box.SIMPLE)

    table.add_column('ID')
    table.add_column('Kind')
    table.add_column('Status')
    table.add_column('Contact')
    table.add_column('Amount', justify='right')
    table.add_column('Paid', justify='right')
    table.add_column('Due')
    table.add_column('Recurrence')
    table.add_column('Category')
    table.add_column('notes')

    for future in futures:
        table.add_row(
            str(future.id),
            future.kind.value,
            future.status.value,
            future.contact or '-',
            _format_money(future.amount),
            _format_money(future.paid),
            str(future.due),
            future.recurrence.value,
            future.category or '-',
            future.notes or '-'
        )

    console.print(table)

@future_app.command()
def see(
    month: int | None = None,
    year: int | None = None,
    ) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        futures = repo.all()

        if month:
            futures = repo.filter(month, year)

    table = Table(title='futures', box=box.SIMPLE)

    table.add_column('')
    table.add_column('', justify='center')
    table.add_column('due')
    table.add_column('contact')
    table.add_column('amount', justify='right')
    table.add_column('paid', justify='right')
    table.add_column('missing', justify='right')
    table.add_column('notes')

    income = 0
    paid_income = 0
    expenses = 0
    paid_expenses = 0

    for future in futures:
        income += future.amount if future.kind.value == 'receivable' else 0
        paid_income += future.paid if future.kind.value == 'receivable' else 0
        expenses += future.amount if future.kind.value == 'payable' else 0
        paid_expenses += future.paid if future.kind.value == 'payable' else 0

        status = '■'
        if future.status.value == 'paid':
            status = f'[green]■[/green]'
        if future.status.value == 'overdue':
            status = f'[red]■[/red]'
        if future.status.value == 'partial':
            status = f'[orange]■[/orange]'

        table.add_row(
            '-' if future.kind.value == 'payable' else '+',
            status,
            future.due.strftime('%d %b %Y'),
            future.contact or '-',
            _format_money(future.amount),
            _format_money(future.paid),
            _format_money(future.outstanding),
            future.notes or '-',
            end_section=True
        )

    totals = (
        f'income [{_format_money(paid_income)} / {_format_money(income)}] /// '
        f'expenses [{_format_money(paid_expenses)} / {_format_money(expenses)}]'
    )

    console.print(
        Group(
            table,
            Align.left(totals)
        ),
        justify='left'
    )


@future_app.command('del')
def delete(id: str) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        is_deleted = repo.delete(id)

    if is_deleted:
        typer.echo('\nDeleted ;)')
    else:
        typer.echo('\nFuture not found :(')

def main():
    app()


def _format_money(amount: int) -> str:
    return f'{amount / 100 :,.2f}'
