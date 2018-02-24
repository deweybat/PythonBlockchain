from flask import Flask
from flask import request
node = Flask(__name__)

this_nodes_transactions = []

@node.route('/transaction', methods=['POST'])
def transaction():
	if request.method == 'POST':
		new_transaction = request.get_json()
		this_nodes_transactions.append(new_transaction)
		
		print "New transaction"
		print "FROM: {}".format(new_transaction['from'])
		print "TO: {}".format(new_transaction['to'])
		print "AMOUNT: {}\n".format(new_transaction['amount'])
		
		return "Transaction submission successful\n"
node.run()
