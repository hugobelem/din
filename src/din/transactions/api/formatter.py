from datetime import date
from din.transactions.core.entity import Transaction, TransactionType


BLACK = "\033[30m"
GRAY = "\033[37m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
REVERSE = "\033[7m"
STRIKE = "\033[9m"

def single(
    t: Transaction,
    category_width: int | None = None,
    amount_width: int | None = None,
):      
    amount = f'{t.amount / 100:,.2f}'

    if category_width is None and amount_width is None:
        return (
            f'{t.created.strftime('%a %-d %b %H:%M %Y')} | '
            f'{t.id} | {t.due} | [ {t.type.value} ] | '
            f'{t.category} | {amount} | {t.description}'
        )

    return (
        f'{t.id} | {t.due} | [ {t.type.value:7} ] | '
        f'{t.category:<{category_width}} | '
        f'{amount:>{amount_width}} | '
        f'{t.description}'
    )

def multiple(transactions: list[Transaction]):
    if not transactions:
        return

    formatted_amounts = [f'{t.amount / 100:,.2f}' for t in transactions]
    amount_width = max(len(a) for a in formatted_amounts)
    category_width = max(len(t.category) for t in transactions)

    month = ''
    group_by_month: dict[str, list[Transaction]] = {}

    for t in transactions:
        month_name = t.due.strftime('%b')

        if month_name != month:
            month = month_name
            group_by_month.update({month: []})

        if month_name in group_by_month.keys():
            group_by_month[month_name].append(t)

    for month, transactions in reversed(group_by_month.items()):
        print(f'{BOLD}{month}{RESET}')
        total_balance = 0
        total_income = 0
        total_expense = 0
        forcasted_income = 0
        forcasted_expense = 0
        for i, t in enumerate(transactions):
            total_balance += t.amount
            if t.type == TransactionType.INCOME:
                total_income += t.amount
            if t.type == TransactionType.EXPENSE:
                total_expense += t.amount

            if t.due > date.today():
                if t.type == TransactionType.INCOME:
                    forcasted_income += t.amount
                if t.type == TransactionType.EXPENSE:
                    forcasted_expense += t.amount
                    
            today = date.today()
            color = RESET
            if t.due > today:
                color = DIM
            if t.due == today:
                color = BOLD
            if t.type == TransactionType.INCOME:
                color += ITALIC

            line = single(
                t,
                category_width=category_width,
                amount_width=amount_width,
            )
            print(f'{color}{i + 1:3}. {line}{RESET}')


        if total_balance > 0:
            color = GREEN
        else:
            color = RED

        print(f'{'-'*100}')
        print(
            'forecast // '
            f'income: {forcasted_income / 100:,.2f} // '
            f'expense: {forcasted_expense / 100:,.2f}'
        )
        print(
            'totals // '
            f'income: {total_income / 100:,.2f} // '
            f'expense: {total_expense / 100:,.2f} // '
            f'balance: {color}{total_balance / 100:,.2f}{RESET}'
        )
        print('')
