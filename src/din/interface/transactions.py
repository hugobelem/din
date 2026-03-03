import typer
from typing import Literal
from din.infra.db import SessionLocal
from din.transactions.utils import formatter
from din.transactions.app.dto import TransactionUpdate
from din.transactions.infra.alchemy import AlchemyTransactionRepository

transaction = typer.Typer(no_args_is_help=True)

@transaction.command()
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

@transaction.command()
def all():
    from din.transactions.app.use import ListTransactions

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = ListTransactions(repo)

        transactions = use.execute()
        transactions.sort(key=lambda t: t.due)

        formatter.multiple(transactions)

@transaction.command()
def get(id: str):
    from din.transactions.app.use import GetTransaction

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTransaction(repo)

        t = use.execute(id)
        
        if t:
            print(formatter.single(t))
        else:
            print('Not found')

@transaction.command()
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

        t = use.execute(id, fields)

        if t:
            print(formatter.single(t))
        else:
            print('Not found')


@transaction.command()
def delete(id: str):
    from din.transactions.app.use import DeleteTransaction

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = DeleteTransaction(repo)

        use.execute(id)

@transaction.command()
def balance():
    from din.transactions.app.use import GetTotalBalance

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalBalance(repo)

        print(f'balance: {use.execute() / 100:.2f}')
