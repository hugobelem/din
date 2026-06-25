import typer

from dataclasses import dataclass
from datetime import date
from calendar import monthrange

from din import settings, future as f

from rich import box
from rich.console import Console, Group
from rich.table import Table
from rich.align import Align


app = typer.Typer()
console = Console()


@dataclass(slots=True)
class FutureTotals:
    income: int = 0
    paid_income: int = 0
    income_missing: int = 0

    expenses: int = 0
    paid_expenses: int = 0
    expenses_missing: int = 0

    @property
    def balance(self) -> int:
        return self.income - self.expenses

    def add(self, other: "FutureTotals") -> None:
        self.income += other.income
        self.paid_income += other.paid_income
        self.income_missing += other.income_missing

        self.expenses += other.expenses
        self.paid_expenses += other.paid_expenses
        self.expenses_missing += other.expenses_missing

    @property
    def formatted(self) -> str:
        return (
            f'income [{_format_money(self.paid_income)} / '
            f'{_format_money(self.income)} → '
            f'{_format_money(self.income_missing)}] /// '
            f'expenses [{_format_money(self.paid_expenses)} / '
            f'{_format_money(self.expenses)} → '
            f'{_format_money(self.expenses_missing)}] /// '
            f'balance {_format_money(self.balance)}'
        )

    @property
    def net(self) -> int:
        return self.income - self.expenses


@app.command()
def add(
    kind: f.Kind = typer.Option('payable'),
    issued: str = typer.Option(date.today()),
    due: str = typer.Option(...),
    amount: int = typer.Option(...),
    paid: int = typer.Option(0),
    category: str = typer.Option(...),
    notes: str = typer.Option(...),
    contact: str = typer.Option(...),
    recurrence: f.Recurrence = typer.Option('once'),
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
            paid=paid,
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

@app.command()
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

@app.command()
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
            future.notes or '-'
        )

    console.print(table)

@app.command()
def month(
    month: int = typer.Argument(date.today().month),
    year: int = typer.Option(date.today().year, '--year', '-y'),
    ) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        futures = repo.by_month(month, year)

    table, totals, _ = _render_futures(
        futures,
        date(year, month, 1).strftime('%b %Y'),
    )

    console.print(
        Group(
            table,
            Align.left(totals.formatted),
        )
    )

@app.command()
def see(
    ) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        futures = repo.all()

    group_by_month: dict[str, list[f.Future]] = {}

    for future in futures:
        month = future.due.strftime('%b %Y')
        group_by_month.setdefault(month, []).append(future)
    
    grand_totals = FutureTotals()
    running_balance = 0

    for month in group_by_month.keys():
        month_futures = group_by_month[month]

        table, totals, running_balance = _render_futures(
            month_futures,
            month,
            running_balance_start=running_balance
        )
        
        grand_totals.add(totals)
        
        console.print(table)

    console.print(Align.left(grand_totals.formatted))

@app.command()
def search(term: str) -> None:
    with settings.Session() as session:
        repo = f.FutureRepository(session)
        results = repo.search(term)

    table = Table(title='Futures', box=box.SIMPLE)

    table.add_column('ID')
    table.add_column('Kind')
    table.add_column('Status')
    table.add_column('Contact')
    table.add_column('Amount', justify='right')
    table.add_column('Paid', justify='right')
    table.add_column('Due')
    table.add_column('notes')

    for r in results:
        table.add_row(
            str(r.id),
            r.kind.value,
            r.status.value,
            r.contact or '-',
            _format_money(r.amount),
            _format_money(r.paid),
            str(r.due),
            r.notes or '-'
        )

    console.print(table)

@app.command('del')
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

def _render_futures(
    futures: list[f.Future],
    title: str,
    running_balance_start: int = 0,
) -> tuple[Table, FutureTotals, int]:
    totals = FutureTotals()
    running_balance = running_balance_start

    table = Table(title=title, box=box.SIMPLE)

    table.add_column('')
    table.add_column('', justify='center')
    table.add_column('due')
    table.add_column('contact')
    table.add_column('amount', justify='right')
    table.add_column('paid', justify='right')
    table.add_column('missing', justify='right')
    table.add_column('balance', justify='right')
    table.add_column('notes')

    for future in futures:
        if future.kind.value == 'receivable':
            totals.income += future.amount
            totals.paid_income += future.paid
            totals.income_missing += future.outstanding
            running_balance += future.amount
        else:
            totals.expenses += future.amount
            totals.paid_expenses += future.paid
            totals.expenses_missing += future.outstanding
            running_balance -= future.amount

        status = '■'
        if future.status.value == 'paid':
            status = '[green]■[/green]'
        elif future.status.value == 'overdue':
            status = '[red]■[/red]'
        elif future.status.value == 'partial':
            status = '[yellow]■[/yellow]'

        if running_balance < 0:
            format_balance = f'[red]{_format_money(running_balance)}[/red]'
        elif running_balance < 100000:
            format_balance = f'[yellow]{_format_money(running_balance)}[/yellow]'
        else:
            format_balance = f'[green]{_format_money(running_balance)}[/green]'

        kind = (
            '[bold][red]-[/red][/bold]'
            if future.kind.value == 'payable'
            else '[bold][green]+[/green][/bold]'
        )

        table.add_row(
            kind,
            status,
            future.due.strftime('%d %b %Y'),
            future.contact or '-',
            _format_money(future.amount),
            _format_money(future.paid),
            _format_money(future.outstanding),
            format_balance,
            future.notes or '-',
            end_section=True,
        )

    return table, totals, running_balance
