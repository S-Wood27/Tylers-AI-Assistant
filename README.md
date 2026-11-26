# Tyler's AI Life & Gig Work Assistant 🚗

## Project Overview

Tyler's AI Life & Gig Work Assistant is an AI-powered chatbot designed to help gig workers manage their work and personal responsibilities.

The application is built around Tyler Bennett, a 27-year-old full-time gig driver who works for RideNow, Hopp, and SnackDash. It helps him stay organized, track his finances, monitor mobile data usage, and balance his work and personal life.

The goal is to provide a simple, centralized assistant that makes managing everyday responsibilities easier.

## Features

### 💬 AI Chatbot
- Provides personalized assistance using the OpenAI API.
- Answers questions about finances, tasks, and responsibilities.
- Uses saved task and transaction information to provide relevant responses.
- Helps prioritize upcoming and overdue tasks.

### 💰 Financial Tracker
- Record income and expenses.
- Categorize transactions.
- Associate transactions with gig-work platforms.
- Filter transactions by day, week, month, or all time.
- View total income, expenses, and net balance.
- Visualize income versus expenses.
- Delete incorrectly entered transactions.

### 📋 Tasks & Reminders
- Create tasks with deadlines and priority levels.
- Mark tasks as completed.
- Identify overdue tasks and tasks due today.
- Display completed tasks differently from outstanding tasks.

### 📱 Mobile Data Usage
- View monthly mobile data usage.
- Monitor remaining data allowance.
- See data consumption by application.
- Generate AI-powered recommendations to reduce mobile data usage.

## Technologies Used

- **Python** – Main programming language.
- **Streamlit** – Web application framework and user interface.
- **OpenAI API** – Powers the AI chatbot and personalized recommendations.
- **SQLite** – Stores application information.
- **python-dotenv** – Loads environment variables securely.

## Database

The application uses SQLite to store information locally.

The database includes four tables:

- **tasks:** Stores task descriptions, deadlines, priorities, and completion status.
- **transactions:** Stores income and expenses, including categories, dates, platforms, and descriptions.
- **events:** Stores scheduled events and activities.
- **goals:** Stores personal goals and descriptions.

The database tables are automatically created when the application starts.

## Limitations

- Mobile data usage is based on the provided Tyler scenario and is not retrieved directly from his phone.
- Financial records must be entered manually.
- The application does not connect directly to gig-work platforms or bank accounts.
- AI responses depend on the information provided to the application.
- An active internet connection and a valid OpenAI API key are required for AI functionality.

## Project Purpose

This project demonstrates how Python, databases, and AI can be combined to develop a practical application that addresses everyday challenges faced by gig workers.