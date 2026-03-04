import typer
from typing import Literal
from din.infra.db import SessionLocal
from din.transactions.utils import formatter
from din.transactions.app.dto import TransactionUpdate
from din.transactions.infra.alchemy import AlchemyTransactionRepository

transaction_app = typer.Typer(no_args_is_help=True)

@transaction_app.command()
def add(
    type: Literal[1, 2 ,3],
    category: str,
    amount: int,
    description: str,
    due: str | None = None,
):
    from din.transactions.app.use import AddTransaction

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = AddTransaction(repo)
        use.execute(type, due, description, amount, category)

@transaction_app.command()
def all():
    from din.transactions.app.use import ListTransactions

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = ListTransactions(repo)

        transactions = use.execute()
        transactions.sort(key=lambda t: t.due)

        formatter.multiple(transactions)

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
    type: int | None = None,
):
    from din.transactions.app.use import UpdateTransaction

    if type and type not in [1, 2, 3]:
        print('Type must be 1 (income), 2 (expense), or 3 (transfer)')
        return

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = UpdateTransaction(repo)

        fields = TransactionUpdate(
            due=due,
            amount=amount,
            category=category,
            description=description,
            type=type
        )

        transaction = use.execute(id, fields)

        if transaction:
            print(formatter.single(transaction))
        else:
            print('Not found')


@transaction_app.command()
def delete(id: str):
    from din.transactions.app.use import DeleteTransaction

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = DeleteTransaction(repo)

        use.execute(id)

@transaction_app.command()
def balance():
    from din.transactions.app.use import GetTotalBalance

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalBalance(repo)

        print(f'balance: {use.execute() / 100:.2f}')
