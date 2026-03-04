import typer
from din.infra.db import SessionLocal
from din.transactions.infra.alchemy import AlchemyTransactionRepository

balance_app = typer.Typer(invoke_without_command=True)
income_app = typer.Typer(invoke_without_command=True)
expense_app = typer.Typer(invoke_without_command=True)
total_app = typer.Typer(invoke_without_command=True)

@balance_app.callback()
def get_tota_balance(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalBalance

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalBalance(repo)

        print(f'balance: {use.execute() / 100:.2f}')

@income_app.callback()
def get_total_income(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalIncome

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalIncome(repo)

        print(f'income: {use.execute() / 100:.2f}')

@expense_app.callback()
def get_total_expense(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotalExpense

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotalExpense(repo)

        print(f'expense: {use.execute() / 100:.2f}')

@total_app.callback()
def get_total(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    
    from din.transactions.app.use import GetTotal

    with SessionLocal() as session:
        repo = AlchemyTransactionRepository(session)
        use = GetTotal(repo)

        print(f'total: {use.execute() / 100:.2f}')
