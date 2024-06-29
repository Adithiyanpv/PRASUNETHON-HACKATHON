import csv
import random
from decimal import Decimal, ROUND_HALF_UP

def round_decimal(value):
    return max(Decimal('0.00'), Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

def generate_transaction(is_fraud):
    transaction_types = ['Payment', 'Transfer', 'Cash-Out', 'Cash-In', 'Debit']
    transaction_type = random.choice(transaction_types)
    
    if is_fraud:
        if random.random() < 0.7:
            amount = round_decimal(random.uniform(5000, 50000))
        else:
            amount = round_decimal(random.uniform(0.01, 1))
    else:
        if transaction_type in ['Payment', 'Debit']:
            amount = round_decimal(random.uniform(10, 1000))
        elif transaction_type == 'Transfer':
            amount = round_decimal(random.uniform(100, 5000))
        elif transaction_type == 'Cash-Out':
            amount = round_decimal(random.uniform(50, 2000))
        else:  # Cash-In
            amount = round_decimal(random.uniform(20, 3000))
    
    initial_balance_sender = round_decimal(random.uniform(0, 20000))
    initial_balance_receiver = round_decimal(random.uniform(0, 20000))
    
    if is_fraud:
        if transaction_type in ['Payment', 'Transfer', 'Cash-Out', 'Debit']:
            if random.random() < 0.6:
                final_balance_sender = round_decimal(Decimal(str(random.uniform(0, float(initial_balance_sender)))))
            else:
                final_balance_sender = round_decimal(max(Decimal('0'), initial_balance_sender - amount * Decimal('1.2')))
        else:
            final_balance_sender = initial_balance_sender
        
        if transaction_type in ['Payment', 'Transfer', 'Cash-In']:
            final_balance_receiver = round_decimal(initial_balance_receiver + amount * Decimal('1.1'))
        else:
            final_balance_receiver = initial_balance_receiver
    else:
        if transaction_type in ['Payment', 'Transfer', 'Cash-Out', 'Debit']:
            final_balance_sender = round_decimal(max(Decimal('0'), initial_balance_sender - amount))
        else:
            final_balance_sender = initial_balance_sender
        
        if transaction_type in ['Payment', 'Transfer', 'Cash-In']:
            final_balance_receiver = round_decimal(initial_balance_receiver + amount)
        else:
            final_balance_receiver = initial_balance_receiver
    
    if not is_fraud and random.random() < 0.01:
        final_balance_sender = round_decimal(final_balance_sender + Decimal(str(random.uniform(0, 1))))
        final_balance_receiver = round_decimal(final_balance_receiver + Decimal(str(random.uniform(0, 1))))
    
    return [
        transaction_type,
        float(amount),
        float(initial_balance_sender),
        float(initial_balance_receiver),
        float(final_balance_sender),
        float(final_balance_receiver),
        1 if is_fraud else 0
    ]

# Generate dataset
num_transactions = 10000
fraud_ratio = 0.4
dataset = []

for _ in range(num_transactions):
    is_fraud = random.random() < fraud_ratio
    dataset.append(generate_transaction(is_fraud))

# Write to CSV
filename = 'realistic_transaction_dataset.csv'
headers = ['Transaction_Type', 'Amount', 'Initial_Balance_Sender', 'Initial_Balance_Receiver', 
           'Final_Balance_Sender', 'Final_Balance_Receiver', 'Fraud']

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(dataset)

print(f"Realistic dataset has been generated and saved as {filename}")