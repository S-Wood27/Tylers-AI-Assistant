import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from database import create_tables, add_transaction, get_transactions, add_task, get_tasks, update_task_status, delete_transaction
from datetime import date, timedelta


# Load API key from .env
load_dotenv()

# Connect to OpenAI
client = OpenAI()

create_tables()

# Configure the application
st.set_page_config(
    page_title="Tyler's AI Assistant",
    page_icon="🚗"
)

# Tyler's AI instructions
INSTRUCTIONS = """
You are Tyler's AI Life and Gig Work Assistant.

Tyler Bennett is 27 years old and works full-time as a gig driver
for RideNow, Hopp, and SnackDash.

Your job is to help Tyler:
- Organize tasks, reminders, and deadlines.
- Track income, expenses, gas receipts, and mileage.
- Understand and reduce mobile data usage.
- Plan work hours, breaks, and personal activities.
- Make time for his girlfriend Jess, the gym, and hobbies.

Be friendly, practical, and supportive.
Keep responses clear and concise.
Give advice that considers Tyler's busy schedule as a gig driver.

Do not pretend to access his phone, apps, bank accounts, or location.
Only use information Tyler provides or information stored in the app.
"""

# Application heading
st.title("🚗 Tyler's AI Assistant")

st.write(
    "Hi Tyler! I'm your personal assistant. "
    "I can help you manage your gig work, "
    "finances, mobile data usage, reminders, and personal life."
)

# Application tabs
chat_tab, finance_tab, tasks_tab, data_tab = st.tabs([
    "💬 Chat",
    "💰 Finances",
    "📋 Tasks",
    "📱 Data Usage"
])

with chat_tab:

    # Initialize conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.info(
            "Hi Tyler! 👋 Ask me about your finances, "
            "upcoming tasks, mobile data usage, or work-life balance."
        )

    # Display all previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input stays at the bottom
    prompt = st.chat_input("How can I help you today?")

    if prompt:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        try:

            # Retrieve Tyler's saved information
            tasks = get_tasks()
            transactions = get_transactions()

            # Get today's date
            today = date.today()
            next_week = today + timedelta(days=7)

            # Create task categories
            overdue_tasks = []
            due_today_tasks = []
            upcoming_tasks = []
            completed_tasks = []

            # Sort tasks by deadline
            for task in tasks:

                task_id = task[0]
                title = task[1]
                deadline = task[2]
                priority = task[3]
                completed = task[4]

                if completed == 1:
                    completed_tasks.append(task)

                elif deadline:

                    task_deadline = date.fromisoformat(deadline)

                    if task_deadline < today:
                        overdue_tasks.append(task)

                    elif task_deadline == today:
                        due_today_tasks.append(task)

                    elif task_deadline <= next_week:
                        upcoming_tasks.append(task)

            # Calculate financial totals
            total_income = sum(
                transaction[3]
                for transaction in transactions
                if transaction[1] == "Income"
            )

            total_expenses = sum(
                transaction[3]
                for transaction in transactions
                if transaction[1] == "Expense"
            )

            balance = total_income - total_expenses

            # Prepare information for the AI
            context = f"""
            Today is {today}.

            Tyler's overdue tasks:
            {overdue_tasks}

            Tyler's tasks due today:
            {due_today_tasks}

            Tyler's upcoming tasks within seven days:
            {upcoming_tasks}

            Tyler's completed tasks:
            {completed_tasks}

            Financial summary:
            Total income: ${total_income:.2f}
            Total expenses: ${total_expenses:.2f}
            Remaining balance: ${balance:.2f}

            Financial transactions:
            {transactions}

            When discussing tasks, distinguish between overdue,
            due today, upcoming, and completed tasks.
            Help Tyler prioritize urgent tasks.
            Do not invent deadlines or task information.
            """

            # Get AI response
            with st.spinner("Thinking..."):

                response = client.responses.create(
                    model="gpt-5.5",
                    instructions=INSTRUCTIONS,
                    input=context + "\n\nConversation:\n" +
                    str(st.session_state.messages[-12:])
                )

                answer = response.output_text

            # Save AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            # Refresh conversation
            st.rerun()

        except Exception as e:
            st.error(
                "I'm having trouble responding right now. "
                "Please check your internet connection and try again."
            )
            print(f"Chatbot error: {e}")

            
with finance_tab:
    st.header("💰 Financial Tracker")

    st.subheader("Add a Transaction")

    with st.form("transaction_form"):

        transaction_type = st.selectbox(
            "Transaction Type",
            ["Income", "Expense"]
        )

        category = st.selectbox(
            "Category",
            ["Delivery", "Ride Earnings", "Gas", "Maintenance", "Other"]
        )

        amount = st.number_input(
            "Amount ($)",
            min_value=0.01,
            step=1.00
        )

        transaction_date = st.date_input("Date")

        platform = st.selectbox(
            "Platform",
            ["None", "RideNow", "Hopp", "SnackDash"]
        )

        description = st.text_input("Description")

        submitted = st.form_submit_button("Save Transaction")

        if submitted:
            if platform == "None":
                platform = None

            add_transaction(
                transaction_type,
                category,
                amount,
                str(transaction_date),
                platform,
                description
            )

            st.success("Transaction saved!")

            st.rerun()


    st.divider()

    

       # Retrieve all transactions
    transactions = get_transactions()

    st.divider()

    # Select financial period
    st.subheader("Financial Summary")

    period = st.selectbox(
        "Select Time Period",
        ["All Time", "Today", "This Week (to date)", "This Month"]
    )

    # Get today's date
    today = date.today()

    # Filter transactions
    filtered_transactions = []

    for transaction in transactions:

        transaction_date = date.fromisoformat(transaction[4])

        if period == "All Time":
            filtered_transactions.append(transaction)

        elif period == "Today" and transaction_date == today:
            filtered_transactions.append(transaction)

        elif period == "This Week (to date)" and transaction_date >= today - timedelta(days=today.weekday()) and transaction_date <= today:
            filtered_transactions.append(transaction)

        elif period == "This Month" and transaction_date.month == today.month and transaction_date.year == today.year:
            filtered_transactions.append(transaction)

    # Calculate income and expenses
    total_income = sum(
        transaction[3]
        for transaction in filtered_transactions
        if transaction[1] == "Income"
    )

    total_expenses = sum(
        transaction[3]
        for transaction in filtered_transactions
        if transaction[1] == "Expense"
    )

    balance = total_income - total_expenses

    # Display totals
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"${total_income:.2f}")
    col2.metric("Total Expenses", f"${total_expenses:.2f}")
    col3.metric("Net Balance", f"${balance:.2f}")

    st.divider()

    st.subheader("Income vs. Expenses")

    chart_data = {
        "Type": ["Income", "Expenses"],
        "Amount": [total_income, total_expenses]
    }

    st.bar_chart(
        chart_data,
        x="Type",
        y="Amount",
        horizontal=True
        
    )

    st.divider()

    # Display transaction history
    st.subheader("Transaction History")

    if filtered_transactions:

        for transaction in filtered_transactions:

            transaction_id = transaction[0]
            transaction_type = transaction[1]
            category = transaction[2]
            amount = transaction[3]
            transaction_date = transaction[4]
            platform = transaction[5]
            description = transaction[6]

            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(
                    f"**{transaction_type}** - "
                    f"${amount:.2f} | {category} | {transaction_date}"
                )

                st.caption(
                    f"Platform: {platform or 'N/A'} | "
                    f"Description: {description or 'N/A'}"
                )

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{transaction_id}"):
                    delete_transaction(transaction_id)
                    st.success("Transaction deleted!")
                    st.rerun()

            st.divider()

    else:
        st.info("No transactions found for this period.")

with tasks_tab:
    st.header("📋 Tasks & Reminders")

    st.subheader("Add a New Task")

    with st.form("task_form"):

        title = st.text_input("Task Description")

        deadline = st.date_input("Deadline")

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        submitted = st.form_submit_button("Save Task")

        if submitted:

            if title.strip() == "":
                st.warning("Please enter a task description.")

            else:
                add_task(
                    title,
                    str(deadline),
                    priority
                )

                st.success("Task saved!")
                st.rerun()

    st.divider()

    st.subheader("Your Tasks")

    tasks = get_tasks()

    if tasks:

        for task in tasks:

            task_id = task[0]
            title = task[1]
            deadline = task[2]
            priority = task[3]
            completed = task[4]

            is_completed = st.checkbox(
                title,
                value=bool(completed),
                key=f"task_{task_id}"
            )

            if is_completed != bool(completed):
                update_task_status(task_id, is_completed)
                st.rerun()

            # Display task status
            if completed:
                st.success("✓ Completed")

            elif deadline and date.fromisoformat(deadline) < date.today():
                st.error("⚠ Overdue")

            elif deadline and date.fromisoformat(deadline) == date.today():
                st.warning("Due today")

            else:
                st.caption("In progress")

            st.caption(
                f"Deadline: {deadline} | Priority: {priority}"
            )

            st.divider()
    else:
        st.info("No tasks have been added yet.")

with data_tab:
    st.header("📱 Mobile Data Usage")

    st.subheader("Monthly Data Plan")

    data_limit = 20.0
    data_used = 18.0
    data_remaining = data_limit - data_used

    col1, col2, col3 = st.columns(3)

    col1.metric("Data Used", f"{data_used} GB")
    col2.metric("Data Limit", f"{data_limit} GB")
    col3.metric("Remaining", f"{data_remaining} GB")

    st.progress(data_used / data_limit)

    st.warning("You have used 90% of your monthly data!")

    st.divider()

    st.subheader("Data Usage by App")

    app_usage = {
        "RideNow": 4.6,
        "Spotify": 4.3,
        "SnackDash": 3.7,
        "YouTube": 2.0,
        "Hopp": 1.5,
        "Google Maps": 0.8,
        "Other Apps": 1.1
    }

    for app, usage in app_usage.items():

        st.write(f"**{app}** - {usage} GB")

        st.progress(usage / data_limit)

    st.divider()

    st.subheader("💡 AI Recommendations")

    st.write(
        "Based on your current data usage, here are some ways "
        "to reduce your mobile data consumption."
    )

    if st.button("Get Recommendations"):

        try:
            with st.spinner("Analyzing your data usage..."):

                response = client.responses.create(
                    model="gpt-5.5",
                    instructions=INSTRUCTIONS,
                    input=f"""
                    Tyler has a 20 GB mobile data plan and has used 18 GB.

                    His app usage:
                    RideNow: 4.6 GB
                    Spotify: 4.3 GB
                    SnackDash: 3.7 GB
                    YouTube: 2.0 GB
                    Hopp: 1.5 GB
                    Google Maps: 0.8 GB

                    Give Tyler three practical recommendations
                    to reduce mobile data usage.
                    Keep the advice short and personalized.
                    """
                )

                st.write(response.output_text)

        except Exception as e:
            st.error(
                "I couldn't generate recommendations right now. "
                "Please try again in a moment."
            )
            print(f"Recommendation error: {e}")

    st.caption("Data usage is based on Tyler's provided scenario information, not live phone data.")