# Banking-ChatBot

python banking_chatbot.py```

You will be greeted by the AI Banking Assistant and can start interacting with it.

## 🤖 How to Use

Once the chatbot is running, you can ask it questions or give it commands.

### Example Interactions

- **Check Balance:**
  > **You:** `What is my account balance?`
  > **Assistant:** `To assist you better, I'll need your account number. Could you please provide your 8-digit account number?`
  > **You:** `My account number is 12345678`
  > **Assistant:** `Hello John Doe! Your account balance is ₹15,000.50.`

- **Apply for a Loan:**
  > **You:** `I want to apply for a personal loan of 50000`
  > **Assistant:** `I need your account number to proceed with this request.`
  > **You:** `12345678`
  > **Assistant:** `Loan Application Processed! Application ID: LOAN...`

- **Block a Card:**
  > **You:** `I need to block my debit card for account 87654321`
  > **Assistant:** `Your debit card has been successfully blocked for security.`

### Special Commands

- `quit`: Exits the application.
- `reset`: Clears the current conversation context (e.g., forgets the account number).
- `context`: Displays the current user context that the chatbot has stored.

## 📂 Code Overview

-   **`BankingChatbot`**: The main class that orchestrates the entire chatbot logic, including the Sense, Reason, Action, and Learn methods.
-   **`MockBankingAPI`**: A mock API class that simulates back-end banking operations. It provides dummy data for accounts, transactions, and interest rates, allowing the chatbot to be tested without a real banking integration.
-   **`main()`**: The entry point for the application, which handles the user interaction loop in the command line.
