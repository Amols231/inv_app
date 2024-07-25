from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        item TEXT,
                        amount INTEGER,
                        quantity INTEGER,
                        total INTEGER)''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view_entries():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM entries ORDER BY date ASC')
        rows = c.fetchall()
        c.execute('SELECT SUM(total) FROM entries')
        grand_total = c.fetchone()[0] or 0
    return render_template('view.html', rows=rows, grand_total=grand_total)

@app.route('/add', methods=['POST'])
def add_entry():
    date = request.form['date']
    item = request.form['item']
    amount = request.form['amount']
    quantity = request.form['quantity']
    total = int(amount) * int(quantity)
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO entries (date, item, amount, quantity, total) VALUES (?, ?, ?, ?, ?)',
                  (date, item, amount, quantity, total))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete-entry/<int:id>', methods=['POST'])
def delete_entry(id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM entries WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('view_entries'))

@app.route('/delete-all-entries', methods=['POST'])
def delete_all_entries():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM entries')
        conn.commit()
    return redirect(url_for('view_entries'))

if __name__ == '__main__':
    # Bind the application to all interfaces on port 8000
    app.run(host='0.0.0.0', port=8000, debug=false)  # Change 8000 to your desired port number
