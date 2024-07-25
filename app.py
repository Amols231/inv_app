from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://database_ycy5_user:y9t5XQhDbxswdCHtXyzBKKffHKjFcl1c@dpg-cqhblt2ju9rs738j0vi0-a:5432/database_ycy5'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    item = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view_entries():
    entries = Entry.query.order_by(Entry.date.asc()).all()
    grand_total = db.session.query(db.func.sum(Entry.total)).scalar() or 0
    return render_template('view.html', rows=entries, grand_total=grand_total)

@app.route('/add', methods=['POST'])
def add_entry():
    date = request.form['date']
    item = request.form['item']
    amount = request.form['amount']
    quantity = request.form['quantity']
    total = int(amount) * int(quantity)
    new_entry = Entry(date=date, item=item, amount=amount, quantity=quantity, total=total)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-entry/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = Entry.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('view_entries'))

@app.route('/delete-all-entries', methods=['POST'])
def delete_all_entries():
    Entry.query.delete()
    db.session.commit()
    return redirect(url_for('view_entries'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
