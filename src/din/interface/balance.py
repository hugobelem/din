import typer
from din.infra.db import SessionLocal
from din.transactions.infra.alchemy import AlchemyTransactionRepository

balance = typer.Typer(invoke_without_command=True)

@balance.callback()
def get(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalBalance

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalBalance(repo)

        print(f'balance: {use.execute() / 100:.2f}')
