from flask import Flask, render_template, request, jsonify
import pymysql
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Database configuration
db_config = {
    'host': '192.168.2.116',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'port': 8000,
    'database': 'demo'
}

# Establish database connection
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS calculations (id INT AUTO_INCREMENT PRIMARY KEY, num1 INT, num2 INT, operation VARCHAR(10), result INT)")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']

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

    return render_template('result.html', num1=num1, num2=num2, operation=operation_symbol, result=result)

@app.route('/dashboard')
def dashboard():
    # Fetch all calculations from the database
    cursor.execute("SELECT * FROM calculations")
    calculations = cursor.fetchall()
    
    # Convert to a list of dictionaries
    calculations_list = [{'id': row[0], 'num1': row[1], 'num2': row[2], 'operation': row[3], 'result': row[4]} for row in calculations]
    
    return render_template('dashboard.html', calculations=calculations_list)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
