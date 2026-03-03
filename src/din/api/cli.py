import typer
from din.infra.db import SessionLocal
from din.transactions.use import AddTransaction
from din.transactions.alchemy import AlchemyTransactionRepository


app = typer.Typer()

@app.command()
def add(description: str, amount: float, category: str, type: str):
    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = AddTransaction(repo)
        use.execute(description, amount, category, type)

@app.command()
def list():
    from din.transactions.use import ListTransactions
    from din.transactions.alchemy import AlchemyTransactionRepository
    from din.infra.db import SessionLocal


    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = ListTransactions(repo)

        transactions = use.execute()

        for t in transactions:
            print(
                f"{t.id} | {t.date} | {t.type} | "
                f"{t.category} | {t.amount} | {t.description}"
            )
