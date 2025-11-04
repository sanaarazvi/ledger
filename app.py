import hashlib
import json
from time import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------- Blockchain ---------------- #
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.accounts = {}  # account_number: {'name': str, 'balance': float}
        self.new_block(previous_hash='0', proof=100)

    # Create a new block
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        block['hash'] = self.hash(block)
        self.current_transactions = []
        self.chain.append(block)
        return block

    # Add a new transaction
    def new_transaction(self, sender_name, account_number, amount):
        if account_number not in self.accounts:
            # Create account if it doesn't exist
            self.accounts[account_number] = {'name': sender_name, 'balance': 0}
        # Update balance
        self.accounts[account_number]['balance'] += float(amount)

        # Fixed receiver (Bank)
        receiver = "BANK"
        self.current_transactions.append({
            'sender': account_number,
            'receiver': receiver,
            'amount': float(amount)
        })
        return account_number

    @staticmethod
    def hash(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        return hashlib.sha256(guess).hexdigest()[:4] == "0000"

# ---------------- Flask ---------------- #
blockchain = Blockchain()

@app.route('/', methods=['GET', 'POST'])
def index():
    account_number = ""
    if request.method == 'POST':
        name = request.form['name']
        account_number_input = request.form['account_number']
        amount = request.form['amount']
        account_number = blockchain.new_transaction(name, account_number_input, amount)
    return render_template('index.html', account_number=account_number)

@app.route('/mine')
def mine():
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_block(proof)
    return redirect(url_for('ledger'))

@app.route('/ledger')
def ledger():
    return render_template('ledger.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
