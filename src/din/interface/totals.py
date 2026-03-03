import typer
from din.infra.db import SessionLocal
from din.transactions.infra.alchemy import AlchemyTransactionRepository

balance = typer.Typer(invoke_without_command=True)
income = typer.Typer(invoke_without_command=True)
expense = typer.Typer(invoke_without_command=True)

@balance.callback()
def get_tota_balance(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalBalance

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalBalance(repo)

        print(f'balance: {use.execute() / 100:.2f}')

@income.callback()
def get_total_income(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalIncome

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalIncome(repo)

        print(f'income: {use.execute() / 100:.2f}')

@expense.callback()
def get_total_expense(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalExpense

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalExpense(repo)

        print(f'expense: {use.execute() / 100:.2f}')
