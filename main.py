from flask import Flask, jsonify, request
import csv

app = Flask(__name__)


def load_data(filename, encoding='utf-8'):
    try:
        with open(filename, encoding=encoding, newline='') as file:
            data = list(csv.DictReader(file))
        return data
    except FileNotFoundError:
        app.logger.error(f"File '{filename}' not found.")
        return []


@app.route('/banks', methods=['GET'])
def get_banks():
    data = load_data('bank_branches.csv')
    if not data:
        return jsonify({'error': 'No data available'}), 500
    
    banks = [{'bank_name': row['bank_name'], 'bank_id': row['bank_id'], 'ifsc': row['ifsc']} for row in data]
    return jsonify(banks)


@app.route('/banks/<branch>', methods=['GET'])
def get_branch_details(branch):
    data = load_data('bank_branches.csv')
    if not data:
        return jsonify({'error': 'No data available'}), 500
    
    branch_name = request.args.get('branch')
    bank_found = False
    branches = []
    
    for row in data:
        if row['branch'] == branch:
            bank_found = True
            if not branch_name or row['branch'] == branch_name:
                branches.append({
                    'bank_name': row['bank_name'],
                    'branch_name': row['branch'],
                    'bank_id': row['bank_id'],
                    'address': row['address'],
                    'city': row['city'],
                    'district': row['district'],
                    'state': row['state'],
                    'ifsc': row['ifsc']
                })
                
    if bank_found:
        if branches:
            return jsonify(branches)
        else:
            return jsonify({'error': 'Branch not found'}), 404
    else:
        return jsonify({'error': 'Bank not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
