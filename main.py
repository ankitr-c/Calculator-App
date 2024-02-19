from flask import Flask, render_template, request, jsonify
import pymysql
from flask_cors import CORS
import os
import cred


app = Flask(__name__)
CORS(app)

db_config = {
    'host': cred.host,
    'user': cred.user,  # Replace with your MySQL username
    'password': cred.password,  # Replace with your MySQL password
    'port': cred.port,
    'database': cred.database
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']

    # Open database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    if operation == 'add':
        result = num1 + num2
        operation_symbol = '+'
    elif operation == 'subtract':
        result = num1 - num2
        operation_symbol = '-'
    elif operation == 'multiply':
        result = num1 * num2
        operation_symbol = 'x'
    elif operation == 'divide':
        if num2 == 0:
            return 'Error: Cannot divide by zero!'
        else:
            result = num1 / num2
            operation_symbol = '/'

    # Insert calculation result into the database
    cursor.execute("INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)", (num1, num2, operation, result))
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()

    return render_template('result.html', num1=num1, num2=num2, operation=operation_symbol, result=result)

@app.route('/dashboard')
def dashboard():
    # Open database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all calculations from the database
    cursor.execute("SELECT * FROM calculations")
    calculations = cursor.fetchall()
    
    # Convert to a list of dictionaries
    calculations_list = [{'id': row[0], 'num1': row[1], 'num2': row[2], 'operation': row[3], 'result': row[4]} for row in calculations]
    
    # Close database connection
    cursor.close()
    conn.close()

    return render_template('dashboard.html', calculations=calculations_list)

if __name__ == '__main__':
    cert='cert.crt'
    key='pk.key'
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',8003)))
