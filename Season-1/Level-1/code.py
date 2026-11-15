'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

MAX_ITEM_AMOUNT = 100_000  # max price of one product / size of one payment
MAX_QUANTITY = 100         # max units of one product in an order
MAX_TOTAL = 1_000_000      # max total payable for one order


def to_money(value):
    # str() first so that 1.1 becomes Decimal('1.1'), not 1.100000000000000088...
    return Decimal(str(value))


def validorder(order: Order):
    payments = Decimal(0)
    expenses = Decimal(0)

    for item in order.items:
        if item.type == 'payment':
            # refunds are negative payments, so negative values are allowed,
            # but out-of-range amounts are ignored
            if -MAX_ITEM_AMOUNT <= item.amount <= MAX_ITEM_AMOUNT:
                payments += to_money(item.amount)
        elif item.type == 'product':
            # quantity must be a whole positive number, price must be positive
            if (isinstance(item.quantity, int)
                    and 0 < item.quantity <= MAX_QUANTITY
                    and 0 < item.amount <= MAX_ITEM_AMOUNT):
                expenses += to_money(item.amount) * item.quantity
        else:
            return "Invalid item type: %s" % item.type

    if expenses > MAX_TOTAL:
        return "Total amount payable for an order exceeded"

    net = payments - expenses
    if net != 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
    else:
        return "Order ID: %s - Full payment received!" % order.id