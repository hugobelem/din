from din.transactions.core.entity import Transaction

def single(
    t: Transaction,
    category_width: int | None = None,
    amount_width: int | None = None,
):
    amount = f"{t.amount / 100:.2f}"

    if category_width is None and amount_width is None:
        return (
            f"{t.id} | {t.due} | [ {t.type.value} ] | "
            f"{t.category} | {amount} | {t.description}"
        )

    return (
        f"{t.id} | {t.due} | [ {t.type.value:7} ] | "
        f"{t.category:<{category_width}} | "
        f"{amount:>{amount_width}} | "
        f"{t.description}"
    )

def multiple(transactions: list[Transaction]):
    if not transactions:
        return

    formatted_amounts = [f"{t.amount / 100:.2f}" for t in transactions]
    amount_width = max(len(a) for a in formatted_amounts)
    category_width = max(len(t.category) for t in transactions)

    for i, t in enumerate(transactions):
        line = single(
            t,
            category_width=category_width,
            amount_width=amount_width,
        )
        print(f"{i + 1}. {line}")
