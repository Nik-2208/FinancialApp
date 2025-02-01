from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

@app.route("/")
def signin():
    return render_template("signin.html")


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

@app.route("/transaction-tracking", methods=["GET", "POST"])
def transaction_tracking():
    # Example of a static list of transactions (replace with your data fetching logic)
    transactions = [
        {"description": "Groceries", "amount": 50.75},
        {"description": "Utilities", "amount": 100.00},
        {"description": "Dining", "amount": 25.50}
    ]
    total_expenses = sum(transaction["amount"] for transaction in transactions)
    return render_template("transaction_tracking.html", transactions=transactions, total_expenses=total_expenses)

@app.route('/pay')
def pay():
    return render_template('pay.html')

@app.route("/scan_qr")
def scan_qr():
    return render_template('scan_qr.html')

@app.route('/refer-and-earn')
def refer_and_earn():
    # Example data, you can replace with actual logic
    referral_link = "https://example.com/referral?code=123ABC"
    earnings = 50.00
    return render_template('refer_and_earn.html', referral_link=referral_link, earnings=earnings)

if __name__ == "__main__":
    app.run(debug=True)
