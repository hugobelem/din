from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from din.transactions.core.entity import Transaction, TransactionType


class Ansi(StrEnum):
    BLACK     = "\033[30m"
    GRAY      = "\033[37m"
    RED       = "\033[31m"
    GREEN     = "\033[32m"
    YELLOW    = "\033[33m"
    BLUE      = "\033[34m"
    RESET     = "\033[0m"
    BOLD      = "\033[1m"
    DIM       = "\033[2m"
    ITALIC    = "\033[3m"
    UNDERLINE = "\033[4m"
    REVERSE   = "\033[7m"
    STRIKE    = "\033[9m"


def colorize(text: str, *codes: Ansi) -> str:
    """Wrap *text* with one or more ANSI codes, always resetting at the end."""
    prefix = "".join(codes)
    return f"{prefix}{text}{Ansi.RESET}"


def format_amount(cents: int) -> str:
    return f"{cents / 100:,.2f}"


def format_date(d: date) -> str:
    return d.strftime("%a %d %b %Y")


@dataclass
class MonthTotals:
    balance:          int = field(default=0)
    income:           int = field(default=0)
    expense:          int = field(default=0)
    forecast_income:  int = field(default=0)
    forecast_expense: int = field(default=0)


def compute_totals(transactions: list[Transaction], today: date) -> MonthTotals:
    totals = MonthTotals()

    for t in transactions:
        totals.balance += t.amount

        if t.type == TransactionType.INCOME:
            totals.income += t.amount
            if t.due > today:
                totals.forecast_income += t.amount

        elif t.type == TransactionType.EXPENSE:
            totals.expense += t.amount
            if t.due > today:
                totals.forecast_expense += t.amount

    return totals


def group_by_month(
    transactions: list[Transaction],
    year_month: tuple[int, int] | None = None,
) -> dict[tuple[int, int], list[Transaction]]:
    groups: dict[tuple[int, int], list[Transaction]] = defaultdict(list)

    for t in transactions:
        groups[(t.due.year, t.due.month)].append(t)

    if year_month:
        groups = {year_month: groups[year_month]}

    return dict(sorted(groups.items()))


def _transaction_codes(t: Transaction, today: date) -> list[Ansi]:
    """Return the ANSI codes that should be applied to a transaction row."""
    codes: list[Ansi] = []

    if t.due > today:
        codes.append(Ansi.DIM)
    elif t.due == today:
        codes.append(Ansi.BOLD)

    if t.type == TransactionType.INCOME:
        codes.append(Ansi.ITALIC)

    return codes


def render_line(
    t: Transaction,
    idx: int,
    *,
    category_width: int,
    amount_width: int,
    today: date,
) -> str:
    line = (
        f"{idx:3}. "
        f"{t.id} | "
        f"{t.due} | "
        f"[ {t.type.value:7} ] | "
        f"{t.category:<{category_width}} | "
        f"{format_amount(t.amount):>{amount_width}} | "
        f"{t.description}"
    )
    codes = _transaction_codes(t, today)
    return colorize(line, *codes) if codes else line


def render_summary(totals: MonthTotals) -> None:
    balance_color = Ansi.GREEN if totals.balance >= 0 else Ansi.RED

    print("-" * 80)
    print(
        f"forecast // "
        f"income: {format_amount(totals.forecast_income)} // "
        f"expense: {format_amount(totals.forecast_expense)}"
    )
    print(
        f"totals // "
        f"income: {format_amount(totals.income)} // "
        f"expense: {format_amount(totals.expense)} // "
        f"balance: {colorize(format_amount(totals.balance), balance_color)}"
    )


def single(t: Transaction) -> str:
    today = date.today()
    return render_line(
        t,
        idx=1,
        category_width=len(t.category),
        amount_width=len(format_amount(t.amount)),
        today=today,
    )


def multiple(
    transactions: list[Transaction],
    year_month: tuple[int, int] | None = None,
) -> None:
    if not transactions:
        return

    today         = date.today()
    amount_width  = max(len(format_amount(t.amount)) for t in transactions)
    category_width = max(len(t.category) for t in transactions)
    groups        = group_by_month(transactions, year_month)

    for (year, month), items in groups.items():
        heading = date(year, month, 1).strftime("%B %Y")
        print(colorize(heading, Ansi.BOLD))

        for idx, t in enumerate(items, start=1):
            print(render_line(t, idx, category_width=category_width, amount_width=amount_width, today=today))

        render_summary(compute_totals(items, today))
        print()
