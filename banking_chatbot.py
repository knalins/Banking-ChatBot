import google.generativeai as genai
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import re

# Configure Google GenAI
genai.configure(api_key='YOUR_GOOGLE_API_KEY')  # Replace with your actual API key
model = genai.GenerativeModel('gemini-pro')

class MockBankingAPI:
    """Mock APIs for banking operations"""
    
    def __init__(self):
        self.accounts = {
            "12345678": {
                "account_number": "12345678",
                "account_type": "Savings",
                "balance": 15000.50,
                "customer_name": "John Doe",
                "phone": "9876543210",
                "email": "john.doe@email.com",
                "credit_score": 750
            },
            "87654321": {
                "account_number": "87654321",
                "account_type": "Current",
                "balance": 25000.75,
                "customer_name": "Jane Smith",
                "phone": "9876543211",
                "email": "jane.smith@email.com",
                "credit_score": 680
            }
        }
        
        self.transactions = {
            "12345678": [
                {"date": "2024-07-25", "type": "Credit", "amount": 5000, "description": "Salary Credit"},
                {"date": "2024-07-24", "type": "Debit", "amount": 1200, "description": "Online Purchase"},
                {"date": "2024-07-23", "type": "Debit", "amount": 500, "description": "ATM Withdrawal"},
                {"date": "2024-07-22", "type": "Credit", "amount": 2000, "description": "Transfer from savings"}
            ]
        }
        
        self.interest_rates = {
            "personal_loan": 10.5,
            "home_loan": 8.75,
            "car_loan": 9.25,
            "savings_account": 4.0,
            "fixed_deposit": 6.5
        }
        
        self.blocked_cards = set()
    
    def get_account_details(self, account_number: str) -> Optional[Dict]:
        """Mock API to get account details"""
        time.sleep(0.5)  # Simulate API delay
        return self.accounts.get(account_number)
    
    def get_transaction_history(self, account_number: str, days: int = 30) -> List[Dict]:
        """Mock API to get transaction history"""
        time.sleep(0.5)
        return self.transactions.get(account_number, [])
    
    def check_credit_score(self, account_number: str) -> int:
        """Mock API to check credit score"""
        time.sleep(0.5)
        account = self.accounts.get(account_number)
        return account["credit_score"] if account else 0
    
    def block_card(self, account_number: str, card_type: str) -> bool:
        """Mock API to block card"""
        time.sleep(0.5)
        card_id = f"{account_number}_{card_type}"
        self.blocked_cards.add(card_id)
        return True
    
    def apply_loan(self, account_number: str, loan_type: str, amount: float) -> Dict:
        """Mock API for loan application"""
        time.sleep(1.0)
        credit_score = self.check_credit_score(account_number)
        
        if credit_score >= 700:
            status = "Approved"
            message = f"Congratulations! Your {loan_type} application for ₹{amount:,.2f} has been approved."
        elif credit_score >= 600:
            status = "Under Review"
            message = f"Your {loan_type} application is under review. We'll contact you within 2-3 business days."
        else:
            status = "Rejected"
            message = f"Unfortunately, your {loan_type} application has been rejected due to low credit score."
        
        return {
            "application_id": f"LOAN{random.randint(100000, 999999)}",
            "status": status,
            "message": message,
            "amount": amount,
            "loan_type": loan_type
        }

class BankingChatbot:
    """Main Banking Chatbot Class implementing Sense -> Reason -> Action -> Learn"""
    
    def __init__(self):
        self.api = MockBankingAPI()
        self.conversation_history = []
        self.user_context = {}
        self.learning_data = []
        
    def sense(self, user_input: str) -> Dict:
        """Sense: Understand user input and extract intent"""
        
        # Use GenAI to classify intent and extract entities
        classification_prompt = f"""
        Analyze this banking customer query and classify it into one of these categories:
        1. BASIC_QUERY - General questions about services, rates, charges
        2. ACCOUNT_QUERY - Balance inquiry, transaction history, account details
        3. SPECIFIC_TASK - Loan application, card blocking, specific actions
        
        User Query: "{user_input}"
        
        Return a JSON response with:
        - category: one of the three categories above
        - intent: specific intent (balance_inquiry, loan_application, card_blocking, etc.)
        - entities: any account numbers, amounts, or specific details mentioned
        - confidence: confidence score 0-1
        
        JSON Response:
        """
        
        try:
            response = model.generate_content(classification_prompt)
            # Parse the response to extract structured data
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                classification = json.loads(json_match.group())
            else:
                # Fallback classification
                classification = self._fallback_classification(user_input)
                
        except Exception as e:
            print(f"GenAI classification error: {e}")
            classification = self._fallback_classification(user_input)
        
        return classification
    
    def _fallback_classification(self, user_input: str) -> Dict:
        """Fallback intent classification using keyword matching"""
        user_input_lower = user_input.lower()
        
        # Define keyword patterns
        account_keywords = ['balance', 'transaction', 'history', 'statement', 'account']
        task_keywords = ['loan', 'block', 'card', 'apply', 'application']
        
        if any(keyword in user_input_lower for keyword in task_keywords):
            category = "SPECIFIC_TASK"
            if 'loan' in user_input_lower:
                intent = "loan_application"
            elif 'block' in user_input_lower and 'card' in user_input_lower:
                intent = "card_blocking"
            else:
                intent = "general_task"
        elif any(keyword in user_input_lower for keyword in account_keywords):
            category = "ACCOUNT_QUERY"
            if 'balance' in user_input_lower:
                intent = "balance_inquiry"
            elif 'transaction' in user_input_lower or 'history' in user_input_lower:
                intent = "transaction_history"
            else:
                intent = "account_details"
        else:
            category = "BASIC_QUERY"
            intent = "general_inquiry"
        
        return {
            "category": category,
            "intent": intent,
            "entities": {},
            "confidence": 0.7
        }
    
    def reason(self, classification: Dict, user_input: str) -> Dict:
        """Reason: Determine what information is needed and what actions to take"""
        
        reasoning_prompt = f"""
        Based on this customer request classification, determine what information is needed:
        
        Category: {classification['category']}
        Intent: {classification['intent']}
        User Input: "{user_input}"
        Current Context: {self.user_context}
        
        Determine:
        1. What information do we need from the user?
        2. What API calls are required?
        3. What is the next best action?
        4. Should we ask for clarification?
        
        Respond in a conversational, helpful banking assistant tone.
        """
        
        try:
            response = model.generate_content(reasoning_prompt)
            reasoning = response.text.strip()
        except Exception as e:
            reasoning = "I understand you need help with banking services. Let me assist you."
        
        # Determine required information based on category
        required_info = []
        api_calls_needed = []
        
        if classification['category'] in ['ACCOUNT_QUERY', 'SPECIFIC_TASK']:
            if 'account_number' not in self.user_context:
                required_info.append('account_number')
        
        if classification['intent'] == 'loan_application':
            api_calls_needed.extend(['get_account_details', 'check_credit_score', 'apply_loan'])
            if 'loan_type' not in self.user_context:
                required_info.append('loan_type')
            if 'loan_amount' not in self.user_context:
                required_info.append('loan_amount')
        
        return {
            "reasoning": reasoning,
            "required_info": required_info,
            "api_calls_needed": api_calls_needed,
            "next_action": "gather_info" if required_info else "execute_task"
        }
    
    def action(self, classification: Dict, reasoning: Dict, user_input: str) -> str:
        """Action: Execute the determined action and provide response"""
        
        category = classification['category']
        intent = classification['intent']
        
        # Handle different categories
        if reasoning['next_action'] == 'gather_info':
            return self._gather_information(reasoning['required_info'])
        
        elif category == 'BASIC_QUERY':
            return self._handle_basic_query(intent, user_input)
        
        elif category == 'ACCOUNT_QUERY':
            return self._handle_account_query(intent)
        
        elif category == 'SPECIFIC_TASK':
            return self._handle_specific_task(intent)
        
        else:
            return "I'm here to help you with your banking needs. Could you please tell me what you'd like to do today?"
    
    def _gather_information(self, required_info: List[str]) -> str:
        """Gather missing information from user"""
        
        if 'account_number' in required_info:
            return "To assist you better, I'll need your account number. Could you please provide your 8-digit account number?"
        
        elif 'loan_type' in required_info:
            return """What type of loan are you interested in? We offer:
• Personal Loan
• Home Loan  
• Car Loan

Please let me know which one you'd prefer."""
        
        elif 'loan_amount' in required_info:
            return "What loan amount are you looking for? Please specify the amount you need."
        
        else:
            return "I need some additional information to help you. What would you like to do today?"
    
    def _handle_basic_query(self, intent: str, user_input: str) -> str:
        """Handle basic queries about services, rates, etc."""
        
        user_input_lower = user_input.lower()
        
        if 'interest' in user_input_lower or 'rate' in user_input_lower:
            rates_info = "Here are our current interest rates:\n"
            for service, rate in self.api.interest_rates.items():
                rates_info += f"• {service.replace('_', ' ').title()}: {rate}% per annum\n"
            return rates_info
        
        elif 'charge' in user_input_lower or 'fee' in user_input_lower:
            return """Our current charges:
• ATM withdrawal (own): Free
• ATM withdrawal (other banks): ₹20 per transaction
• SMS alerts: ₹25 per month
• Cheque book: ₹200 per booklet
• Account maintenance: ₹500 per quarter (waived for minimum balance ≥ ₹10,000)"""
        
        else:
            return """I'm here to help you with:
• Account balance and transaction inquiries
• Loan applications (Personal, Home, Car loans)
• Card blocking services
• Interest rates and charges information

What would you like to know about?"""
    
    def _handle_account_query(self, intent: str) -> str:
        """Handle account-related queries"""
        
        account_number = self.user_context.get('account_number')
        if not account_number:
            return "I need your account number to fetch your account details."
        
        account_details = self.api.get_account_details(account_number)
        if not account_details:
            return "I couldn't find an account with that number. Please check and try again."
        
        if intent == 'balance_inquiry':
            return f"""Hello {account_details['customer_name']}! 
            
Your account balance details:
• Account Number: {account_details['account_number']}
• Account Type: {account_details['account_type']}
• Available Balance: ₹{account_details['balance']:,.2f}

Is there anything else I can help you with?"""
        
        elif intent == 'transaction_history':
            transactions = self.api.get_transaction_history(account_number)
            if not transactions:
                return "No recent transactions found for your account."
            
            trans_text = f"Here are your recent transactions for account {account_number}:\n\n"
            for trans in transactions[:5]:  # Show last 5 transactions
                trans_text += f"• {trans['date']} - {trans['type']} - ₹{trans['amount']:,.2f} - {trans['description']}\n"
            
            return trans_text
        
        else:
            return f"""Account Details for {account_details['customer_name']}:
• Account Number: {account_details['account_number']}
• Account Type: {account_details['account_type']}
• Balance: ₹{account_details['balance']:,.2f}
• Email: {account_details['email']}
• Phone: {account_details['phone']}"""
    
    def _handle_specific_task(self, intent: str) -> str:
        """Handle specific banking tasks"""
        
        account_number = self.user_context.get('account_number')
        if not account_number:
            return "I need your account number to proceed with this request."
        
        if intent == 'loan_application':
            loan_type = self.user_context.get('loan_type')
            loan_amount = self.user_context.get('loan_amount')
            
            if not loan_type or not loan_amount:
                missing = []
                if not loan_type:
                    missing.append("loan type")
                if not loan_amount:
                    missing.append("loan amount")
                return f"I need the {' and '.join(missing)} to process your loan application."
            
            # Process loan application
            try:
                loan_amount_float = float(loan_amount.replace(',', '').replace('₹', ''))
                result = self.api.apply_loan(account_number, loan_type, loan_amount_float)
                
                response = f"""Loan Application Processed!
                
Application ID: {result['application_id']}
Status: {result['status']}

{result['message']}

Your credit score: {self.api.check_credit_score(account_number)}

Is there anything else I can help you with?"""
                return response
                
            except ValueError:
                return "Please provide a valid loan amount in numbers."
        
        elif intent == 'card_blocking':
            card_type = self.user_context.get('card_type', 'debit')
            success = self.api.block_card(account_number, card_type)
            
            if success:
                return f"""Your {card_type} card has been successfully blocked for security.

• Card Status: BLOCKED
• Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Reason: Customer Request

A new card will be dispatched to your registered address within 5-7 business days.

For immediate assistance, please contact our 24/7 helpline.
Is there anything else I can help you with?"""
            else:
                return "I couldn't block your card at the moment. Please try again or contact customer service."
        
        else:
            return "I can help you with loan applications or card blocking. What would you like to do?"
    
    def learn(self, user_input: str, classification: Dict, response: str):
        """Learn: Store interaction data for improvement"""
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "classification": classification,
            "response": response,
            "user_context": self.user_context.copy()
        }
        
        self.learning_data.append(interaction)
        self.conversation_history.append({
            "user": user_input,
            "bot": response,
            "timestamp": datetime.now().isoformat()
        })
    
    def extract_entities(self, user_input: str):
        """Extract entities like account numbers, amounts from user input"""
        
        # Account number pattern (8 digits)
        account_match = re.search(r'\b\d{8}\b', user_input)
        if account_match:
            self.user_context['account_number'] = account_match.group()
        
        # Amount pattern
        amount_match = re.search(r'₹?[\d,]+(?:\.\d{2})?', user_input)
        if amount_match:
            self.user_context['loan_amount'] = amount_match.group()
        
        # Loan type
        loan_types = ['personal loan', 'home loan', 'car loan', 'personal', 'home', 'car']
        for loan_type in loan_types:
            if loan_type in user_input.lower():
                self.user_context['loan_type'] = loan_type.replace(' loan', '').title() + ' Loan'
                break
        
        # Card type
        if 'credit card' in user_input.lower():
            self.user_context['card_type'] = 'credit'
        elif 'debit card' in user_input.lower():
            self.user_context['card_type'] = 'debit'
    
    def chat(self, user_input: str) -> str:
        """Main chat function implementing the complete flow"""
        
        print(f"\n🤖 Processing: {user_input}")
        
        # Extract entities from user input
        self.extract_entities(user_input)
        
        # SENSE: Understand user intent
        classification = self.sense(user_input)
        print(f"📊 Classification: {classification}")
        
        # REASON: Determine required actions
        reasoning = self.reason(classification, user_input)
        print(f"🧠 Reasoning: Next action - {reasoning['next_action']}")
        
        # ACTION: Execute and respond
        response = self.action(classification, reasoning, user_input)
        
        # LEARN: Store interaction for improvement
        self.learn(user_input, classification, response)
        
        return response

def main():
    """Main function to run the banking chatbot"""
    
    print("🏦 Welcome to AI Banking Assistant!")
    print("=" * 50)
    print("I can help you with:")
    print("• Account balance and transaction inquiries")
    print("• Loan applications (Personal, Home, Car)")
    print("• Card blocking services")
    print("• Interest rates and charges information")
    print("=" * 50)
    
    chatbot = BankingChatbot()
    
    print("\n💬 Hi! I'm your AI banking assistant. How can I help you today?")
    print("(Type 'quit' to exit, 'reset' to clear context)")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 Thank you for using AI Banking Assistant. Have a great day!")
                break
            
            elif user_input.lower() == 'reset':
                chatbot.user_context = {}
                print("\n🤖 Context cleared. How can I help you?")
                continue
            
            elif user_input.lower() == 'context':
                print(f"\n📋 Current Context: {chatbot.user_context}")
                continue
            
            elif not user_input:
                print("\n🤖 I'm here to help! Please tell me what you need assistance with.")
                continue
            
            # Get response from chatbot
            response = chatbot.chat(user_input)
            print(f"\n🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🤖 Thank you for using AI Banking Assistant. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Sorry, I encountered an error: {e}")
            print("Please try again or contact customer support.")

if __name__ == "__main__":
    main()