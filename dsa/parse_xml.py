"""
XML Parser for Mobile Money SMS Data
Extracts transaction details from SMS messages
"""

import xml.etree.ElementTree as ET
import json
import re


class TransactionParser:
    """Parse mobile money SMS transactions from XML"""

    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.transactions = []

    def parse(self):
        """Parse XML and extract transaction data"""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()

            for i, sms in enumerate(root.findall('sms')):
                tx = self._extract_transaction(sms, i + 1)
                if tx:
                    self.transactions.append(tx)

            return self.transactions

        except Exception as e:
            print(f"Parse error: {e}")
            return []

    def _extract_transaction(self, sms, index):
        """Extract transaction details from SMS"""
        body = sms.get('body', '')

        tx = {
            'id': index,
            'sms_id': sms.get('id', ''),
            'date': sms.get('readable_date', ''),
            'address': sms.get('address', ''),
            'body': body,
            'type': self._get_type(body),
            'amount': 0.0,
            'currency': 'RWF',
            'sender': '',
            'receiver': '',
            'balance': 0.0,
            'fee': 0.0,
            'transaction_id': ''
        }

        # Extract details based on type
        if tx['type'] == 'received':
            self._extract_received(tx)
        elif tx['type'] == 'transfer':
            self._extract_transfer(tx)
        elif tx['type'] == 'payment':
            self._extract_payment(tx)
        elif tx['type'] == 'deposit':
            self._extract_deposit(tx)
        elif tx['type'] == 'airtime':
            self._extract_airtime(tx)

        return tx

    def _get_type(self, body):
        """Determine transaction type"""
        body_lower = body.lower()
        if 'received' in body_lower:
            return 'received'
        elif 'transferred' in body_lower:
            return 'transfer'
        elif 'payment' in body_lower:
            return 'payment'
        elif 'deposit' in body_lower:
            return 'deposit'
        elif 'airtime' in body_lower:
            return 'airtime'
        return 'other'

    def _extract_received(self, tx):
        """Extract received money details"""
        # Amount: "received 2000 RWF"
        amount_match = re.search(r'received (\d+) RWF', tx['body'])
        if amount_match:
            tx['amount'] = float(amount_match.group(1))

        # Sender: "from Jane Smith"
        sender_match = re.search(r'from ([A-Za-z\s]+)\s*\(', tx['body'])
        if sender_match:
            tx['sender'] = sender_match.group(1).strip()

        # Balance: "new balance:2000 RWF"
        balance_match = re.search(r'balance:(\d+)\s*RWF', tx['body'])
        if balance_match:
            tx['balance'] = float(balance_match.group(1))

        # Transaction ID
        tx_match = re.search(r'Transaction Id:\s*(\d+)', tx['body'])
        if tx_match:
            tx['transaction_id'] = tx_match.group(1)

    def _extract_transfer(self, tx):
        """Extract transfer details"""
        # Amount: "1000 RWF transferred"
        amount_match = re.search(r'(\d+)\s*RWF transferred', tx['body'])
        if amount_match:
            tx['amount'] = float(amount_match.group(1))

        # Receiver: "to Samuel Carter"
        receiver_match = re.search(r'to ([A-Za-z\s]+)\s*\(', tx['body'])
        if receiver_match:
            tx['receiver'] = receiver_match.group(1).strip()

        # Fee: "Fee was: 100 RWF"
        fee_match = re.search(r'Fee was:\s*(\d+)\s*RWF', tx['body'])
        if fee_match:
            tx['fee'] = float(fee_match.group(1))

        # Balance: "New balance: 4080 RWF"
        balance_match = re.search(r'balance:\s*(\d+)\s*RWF', tx['body'])
        if balance_match:
            tx['balance'] = float(balance_match.group(1))

    def _extract_payment(self, tx):
        """Extract payment details"""
        # Amount: "payment of 1,000 RWF"
        amount_match = re.search(r'payment of ([\d,]+)\s*RWF', tx['body'])
        if amount_match:
            tx['amount'] = float(amount_match.group(1).replace(',', ''))

        # Receiver: "to Jane Smith"
        receiver_match = re.search(r'to ([A-Za-z\s]+)\s*\d+', tx['body'])
        if receiver_match:
            tx['receiver'] = receiver_match.group(1).strip()

        # Balance: "new balance: 1,000 RWF"
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', tx['body'])
        if balance_match:
            tx['balance'] = float(balance_match.group(1).replace(',', ''))

        # Transaction ID
        tx_match = re.search(r'TxId:\s*(\d+)', tx['body'])
        if tx_match:
            tx['transaction_id'] = tx_match.group(1)

    def _extract_deposit(self, tx):
        """Extract deposit details"""
        # Amount: "deposit of 40000 RWF"
        amount_match = re.search(r'deposit of (\d+)\s*RWF', tx['body'])
        if amount_match:
            tx['amount'] = float(amount_match.group(1))

        # Balance: "NEW BALANCE :40400 RWF"
        balance_match = re.search(r'BALANCE\s*:(\d+)\s*RWF', tx['body'])
        if balance_match:
            tx['balance'] = float(balance_match.group(1))

    def _extract_airtime(self, tx):
        """Extract airtime purchase details"""
        # Amount: "payment of 2000 RWF"
        amount_match = re.search(r'payment of (\d+)\s*RWF', tx['body'])
        if amount_match:
            tx['amount'] = float(amount_match.group(1))

        # Balance: "new balance: 25280 RWF"
        balance_match = re.search(r'balance:\s*([\d,]+)\s*RWF', tx['body'])
        if balance_match:
            tx['balance'] = float(balance_match.group(1).replace(',', ''))

    def save_json(self, filename='transactions.json'):
        """Save parsed data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.transactions, f, indent=2)
            print(f"Saved {len(self.transactions)} transactions to {filename}")
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False


if __name__ == "__main__":
    parser = TransactionParser('modified_sms_v2.xml')
    transactions = parser.parse()

    if transactions:
        print(f"\nParsed {len(transactions)} transactions")
        print(f"\nSample transaction:")
        print(json.dumps(transactions[7], indent=2))

        parser.save_json()