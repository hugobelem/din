import typer
from datetime import datetime
from din.shared.infra.db import SessionLocal
from din.shared.infra.clock import SystemClock
from din.transactions.api.cli import formatter
from din.transactions.app.dto import TransactionUpdate
from din.transactions.infra.alchemy import AlchemyTransactionRepository

transaction_app = typer.Typer(no_args_is_help=True)

@transaction_app.command()
def add(
    type: str,
    category: str,
    amount: int,
    description: str,
    due: str | None = None,
):
    from din.transactions.app.use import AddTransaction
    from din.transactions.core.entity import TransactionType

    parsed_type = TransactionType[type.upper()]

    parsed_due = None
    if due:
        parsed_due = datetime.strptime(due, "%Y-%m-%d").date()
        
    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        clock = SystemClock()
        use = AddTransaction(repo, clock)
        use.execute(parsed_type, parsed_due, description, amount, category)

@transaction_app.command()
def all(year: int | None = 2026, month: int | None = None):
    from din.transactions.app.use import ListTransactions

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = ListTransactions(repo)

        transactions = use.execute()
        transactions.sort(key=lambda t: t.due)

        year_month = None
        if year is not None and month is not None:
            year_month = (year, month)

        formatter.multiple(transactions, year_month)

@transaction_app.command()
def get(id: str):
    from din.transactions.app.use import GetTransaction

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTransaction(repo)

        transaction = use.execute(id)
        
        if transaction:
            print(formatter.single(transaction))
        else:
            print('Not found')

@transaction_app.command()
def update(
    id: str,
    amount: int | None = None,
    due: str | None = None,
    category: str | None = None,
    description: str | None = None,
    type: str | None = None,
):
    from din.transactions.app.use import UpdateTransaction
    from din.transactions.core.entity import TransactionType

    parsed_type = None
    if type:
        parsed_type = TransactionType[type.upper()]

    parsed_due = None
    if due:
        parsed_due = datetime.strptime(due, "%Y-%m-%d").date()

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = UpdateTransaction(repo)

        fields = TransactionUpdate(
            due=parsed_due,
            amount=amount,
            category=category,
            description=description,
            type=parsed_type
        )

        transaction = use.execute(id, fields)

        if transaction:
            print(formatter.single(transaction))
        else:
            print('Not found')


@transaction_app.command()
def delete(ids: list[str]):
    from din.transactions.app.use import DeleteTransaction

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = DeleteTransaction(repo)

        for id in ids:
            use.execute(id)
