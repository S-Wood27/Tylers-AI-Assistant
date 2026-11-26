
from database import (
    create_tables,
    add_task,
    get_tasks,
    add_transaction,
    get_transactions

)

# Create database tables
create_tables()

# Add a sample task
add_task(
    "Review nursing lecture notes",
    "2026-11-17",
    "High"
)

# Retrieve tasks
tasks = get_tasks()

# Display tasks
for task in tasks:
    print(task)

# Add sample income
add_transaction(
    "Income",
    "Delivery",
    120.00,
    "2026-11-23",
    "SnackDash",
    "Food deliveries"
)

# Add sample expense
add_transaction(
    "Expense",
    "Gas",
    55.00,
    "2026-11-23",
    None,
    "Fuel refill"
)

# Retrieve transactions
transactions = get_transactions()

# Display transactions
for transaction in transactions:
    print(transaction)
