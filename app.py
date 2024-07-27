from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    
    conn.execute('''CREATE TABLE IF NOT EXISTS entries
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    item TEXT,
                    amount INTEGER,
                    quantity INTEGER,
                    total INTEGER);''')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-entry', methods=['POST'])
def add_entry():
    if request.method == 'POST':
        date = request.form['date']
        item = request.form['item']
        amount = request.form['amount']
        quantity = request.form['quantity']
        total = int(amount) * int(quantity)

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO entries (date, item, amount, quantity, total) VALUES (?, ?, ?, ?, ?)",
                        (date, item, amount, quantity, total))
            con.commit()
        return redirect(url_for('index'))

@app.route('/view')
def view():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # Fetch and sort entries by date old to new
    cur.execute("SELECT * FROM entries ORDER BY date ASC")
    rows = cur.fetchall()

    # Calculate grand total
    grand_total = sum(row['total'] for row in rows)

    return render_template('view.html', rows=rows, grand_total=grand_total)

@app.route('/delete-entry/<int:id>', methods=['POST'])
def delete_entry(id):
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM entries WHERE id = ?", (id,))
        con.commit()
    return redirect(url_for('view'))

@app.route('/delete-all-entries', methods=['POST'])
def delete_all_entries():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM entries")
        con.commit()
    return redirect(url_for('view'))

if __name__ == '__main__':
    app.run((host='0.0.0.0',port=8000)
