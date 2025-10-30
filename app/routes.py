from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Transaction

main = Blueprint('main', __name__)

@main.route('/')
def index():
    transactions = Transaction.query.all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    return render_template('index.html', transactions=transactions, balance=balance)

@main.route('/add', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = float(request.form['amount'])
    type_ = request.form['type']

    new_transaction = Transaction(description=description, amount=amount, type=type_)
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/delete/<int:id>')
def delete_transaction(id):
    t = Transaction.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('main.index'))

# NEW chart route
@main.route('/chart')
def chart():
    transactions = Transaction.query.all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')

    chart_data = {
        'income': total_income,
        'expense': total_expense
    }

    return render_template('chart.html', chart_data=chart_data)
