import typer
from typing import Literal
from din.infra.db import SessionLocal
from din.transactions.app.use import AddTransaction
from din.transactions.infra.alchemy import AlchemyTransactionRepository


app = typer.Typer()

@app.command()
def add(type: Literal[1, 2 ,3], description: str, amount: int, category: str):
    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = AddTransaction(repo)
        use.execute(description, amount, category, type)

@app.command()
def list():
    from din.transactions.app.use import ListTransactions
    from din.transactions.infra.alchemy import AlchemyTransactionRepository
    from din.infra.db import SessionLocal


    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = ListTransactions(repo)

        transactions = use.execute()

        for i, t in enumerate(transactions):
            print(
                f"{i + 1}. {t.id} | {t.date.date()} | [ {t.type} ] | "
                f"{t.category:12} | {t.amount / 100:<8.2f} | {t.description}"
            )
