# 🏦 AI Banking Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google GenAI](https://img.shields.io/badge/Google-GenAI-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

A conversational AI banking assistant powered by Google GenAI that handles various banking operations through natural language interaction. Built with a **Sense → Reason → Action → Learn** framework for intelligent customer service.

<div align="center">
  <img src="https://via.placeholder.com/800x400/1e3a8a/ffffff?text=AI+Banking+Chatbot" alt="Banking Chatbot Demo" />
</div>

## ✨ Features

- 🤖 **Intelligent Intent Classification** - Automatically understands customer requests
- 💬 **Human-like Conversations** - Natural language processing with context awareness
- 🏧 **Complete Banking Services** - Account management, loans, card services
- 🔄 **Multi-turn Conversations** - Maintains context across interactions
- 🛡️ **Secure Processing** - Mock APIs simulate real banking security
- 📊 **Learning System** - Continuously improves from interactions
- ⚡ **Real-time Processing** - Instant responses with realistic delays

## 🎯 Supported Banking Operations

| Category | Services |
|----------|----------|
| **Account Services** | Balance inquiry, Transaction history, Account details |
| **Loan Services** | Personal loans, Home loans, Car loans with credit checks |
| **Card Services** | Card blocking, New card requests |
| **Information** | Interest rates, Service charges, General banking info |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google GenAI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/banking-chatbot.git
   cd banking-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install google-generativeai
   ```

3. **Configure API Key**
   ```python
   # Edit banking_chatbot.py line 10
   genai.configure(api_key='YOUR_GOOGLE_API_KEY')
   ```

4. **Run the chatbot**
   ```bash
   python banking_chatbot.py
   ```

## 💬 Demo Conversations

### Account Balance Inquiry
```
👤 User: Check my account balance
🤖 Bot: I'll need your account number. Could you please provide your 8-digit account number?
👤 User: 12345678
🤖 Bot: Hello John Doe! 

Your account balance details:
• Account Number: 12345678
• Account Type: Savings
• Available Balance: ₹15,000.50

Is there anything else I can help you with?
```

### Loan Application
```
👤 User: I want to apply for a personal loan of 5 lakhs
🤖 Bot: I'll need your account number to proceed with this request.
👤 User: 12345678
🤖 Bot: Loan Application Processed!

Application ID: LOAN123456
Status: Approved

Congratulations! Your Personal Loan application for ₹5,00,000.00 has been approved.
Your credit score: 750
```

### Card Blocking
```
👤 User: Block my debit card immediately
🤖 Bot: I need your account number to proceed with this request.
👤 User: 12345678
🤖 Bot: Your debit card has been successfully blocked for security.

• Card Status: BLOCKED
• Date & Time: 2024-07-27 14:30:25
• Reason: Customer Request

A new card will be dispatched to your registered address within 5-7 business days.
```

## 🏗️ Architecture

The system implements a sophisticated **Sense → Reason → Action → Learn** framework:

```mermaid
graph TD
    A[User Input] --> B[SENSE: Intent Classification]
    B --> C[REASON: Action Planning]
    C --> D[ACTION: Task Execution]
    D --> E[LEARN: Data Storage]
    E --> F[Response to User]
    
    B --> G[Google GenAI]
    C --> H[Context Management]
    D --> I[Mock Banking APIs]
    E --> J[Conversation History]
```

### Core Components

- **🧠 BankingChatbot**: Main orchestrator implementing the SRAL framework
- **🏦 MockBankingAPI**: Realistic banking service simulation
- **🎯 Intent Classifier**: Three-tier classification system
- **💾 Context Manager**: Maintains conversation state
- **📚 Learning System**: Stores interactions for improvement

## 📊 Intent Classification System

The chatbot categorizes all requests into three intelligent tiers:

| Tier | Category | Examples | Requirements |
|------|----------|----------|--------------|
| 1 | **Basic Query** | Interest rates, charges, general info | None |
| 2 | **Account Query** | Balance, transactions, account details | Account number |
| 3 | **Specific Task** | Loan applications, card blocking | Account + additional info |

## 🛠️ Technical Details

### Built With
- **Python 3.8+** - Core language
- **Google GenAI** - Natural language understanding
- **Mock APIs** - Banking service simulation
- **JSON** - Data serialization
- **Regex** - Entity extraction

### Key Classes

#### `BankingChatbot`
Main conversation handler implementing the SRAL framework.

```python
def chat(self, user_input: str) -> str:
    classification = self.sense(user_input)      # Understand intent
    reasoning = self.reason(classification)      # Plan actions
    response = self.action(reasoning)            # Execute tasks
    self.learn(user_input, response)            # Store interaction
    return response
```

#### `MockBankingAPI`
Comprehensive banking service simulation with realistic data and processing.

```python
# Sample account data
accounts = {
    "12345678": {
        "customer_name": "John Doe",
        "balance": 15000.50,
        "credit_score": 750
    }
}
```

## 🔧 Configuration

### Environment Variables (Recommended)
```bash
# .env file
GOOGLE_API_KEY=your_actual_api_key_here
```

### Custom Mock Data
Modify `MockBankingAPI.__init__()` to add:
- More customer accounts
- Additional transaction history
- Custom interest rates
- Different credit scores

## 🧪 Testing

### Manual Testing
Use these commands during conversation:
- `quit` - Exit the chatbot
- `reset` - Clear conversation context
- `context` - View current conversation state

### Sample Test Accounts
| Account Number | Customer | Balance | Credit Score |
|----------------|----------|---------|--------------|
| 12345678 | John Doe | ₹15,000.50 | 750 |
| 87654321 | Jane Smith | ₹25,000.75 | 680 |

### Unit Testing
```bash
python -m pytest tests/
```

## 📈 Performance Features

- **⚡ Fast Response**: Average response time < 2 seconds
- **🧠 Context Awareness**: Remembers conversation history
- **🔄 Error Recovery**: Graceful handling of invalid inputs
- **📊 Learning**: Improves from each interaction
- **🛡️ Security**: Input validation and sanitization

## 🚀 Production Deployment

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "banking_chatbot.py"]
```

### Web Service (Flask)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)
bot = BankingChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    response = bot.chat(message)
    return jsonify({'response': response})
```

### Cloud Deployment
- **Google Cloud Run** - Serverless containers
- **AWS Lambda** - Function-as-a-Service
- **Azure Container Instances** - Container hosting

## 📚 Documentation

- [📖 Complete Documentation](docs/README.md) - Comprehensive guide
- [🔧 API Reference](docs/api.md) - Method documentation
- [🚀 Deployment Guide](docs/deployment.md) - Production setup
- [🧪 Testing Guide](docs/testing.md) - Testing strategies

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Include unit tests for new features
- Update documentation for changes
- Test with multiple conversation scenarios

## 🐛 Issues & Support

- 🐞 **Bug Reports**: [Create an issue](https://github.com/yourusername/banking-chatbot/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/yourusername/banking-chatbot/discussions)
- 📧 **Support**: support@yourcompany.com

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Core banking operations
- ✅ Google GenAI integration
- ✅ Mock API system
- ✅ Context management
- ✅ Learning framework

### Planned Features
- 🔄 Real banking API integration
- 🌐 Web interface
- 📱 Mobile app support
- 🔐 Enhanced security features
- 📊 Analytics dashboard

## 🏆 Acknowledgments

- [Google GenAI](https://ai.google.dev/) - For powerful language understanding
- [Python Community](https://www.python.org/) - For excellent libraries and tools
- Banking industry experts - For domain knowledge and requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/banking-chatbot&type=Date)](https://star-history.com/#yourusername/banking-chatbot&Date)

---

<div align="center">



# Banking-ChatBot

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
