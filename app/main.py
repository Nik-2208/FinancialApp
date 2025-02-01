from flask import Flask, render_template, request, redirect, url_for, session
from app.db.database import db, User, Transaction

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_app.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
@app.route('/create_dummy_data')
def create_dummy_data():
    # Create some dummy users
    user1 = User(email='user1@example.com', password='password123')
    user2 = User(email='user2@example.com', password='password123')
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create some dummy transactions for each user
    transaction1 = Transaction(date='2025-01-30', description='YouTube Music', category='Entertainment', amount=-10.99, user_id=user1.id)
    transaction2 = Transaction(date='2025-01-28', description='Salary Payment', category='Income', amount=4500.00, user_id=user1.id)
    transaction3 = Transaction(date='2025-01-25', description='Amazon Purchase', category='Shopping', amount=-150.00, user_id=user2.id)
    
    db.session.add(transaction1)
    db.session.add(transaction2)
    db.session.add(transaction3)
    db.session.commit()

    return "Dummy data created!"
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('signin.html', error="Invalid email or password")
    
    return render_template('signin.html')
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signin'))

    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user.id).all()

    # Calculate totals for the overview cards
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expenses = sum(t.amount for t in transactions if t.category != 'Income')
    net_profit = total_income - total_expenses
    wallet_balance = total_income - total_expenses  # This can be customized further if needed
    
    # Calculate financial distribution percentages for the chart
    savings_percentage = (total_income * 0.4)  # Example: 40% of total income
    investments_percentage = (total_income * 0.35)  # Example: 35% of total income
    expenses_percentage = (total_income * 0.25)  # Example: 25% of total income

    return render_template(
        'dashboard.html', 
        total_income=total_income, 
        total_expenses=total_expenses, 
        net_profit=net_profit,
        wallet_balance=wallet_balance,
        transactions=transactions,
        savings_percentage=savings_percentage,
        investments_percentage=investments_percentage,
        expenses_percentage=expenses_percentage
    )

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        recipient_email = request.form['recipient']
        amount = float(request.form['amount'])
        
        # Example: Dummy logic for finding recipient
        recipient = User.query.filter_by(email=recipient_email).first()
        if recipient:
            transaction = Transaction(
                date='2025-02-01', description=f"Payment to {recipient_email}", category='Payment', amount=-amount, user_id=user_id)
            db.session.add(transaction)
            db.session.commit()
        
        return redirect(url_for('dashboard'))

    return render_template('pay.html')
