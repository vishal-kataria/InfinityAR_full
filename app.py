from flask import Flask, abort, request, render_template,  jsonify
from misc import load_razorpay_credentials, load_user_data, save_user_data
app = Flask(__name__)
import razorpay

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/charge', methods=['POST'])
def charge():
    try:
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Create Razorpay order
        order_amount = 1999 * 100  # Amount in paise
        order_currency = 'INR'
        order_receipt = 'Infinity AR'

        # Razorpay API credentials
        RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET = load_razorpay_credentials()

        # Razorpay client instance
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        payment_order = client.order.create({
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt
        })

        # Pass order details to client
        return jsonify({
            'order_id': payment_order['id'],
            'key_id': RAZORPAY_KEY_ID,
            'name': name,
            'email': email,
            'phone': phone,
            'amount': order_amount
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/success')
def success():
    if request.method != 'POST':
        abort(403)
    try:
        order_id = request.args.get('order_id')
        payment_id = request.args.get('payment_id')
        name = request.args.get('name')
        email = request.args.get('email')
        phone = request.args.get('phone')
        user_data = load_user_data()
        user_data.append({
            "name": name,
            "email": email,
            "phone": phone,
            "order_id": order_id,
            "payment_id": payment_id
        })
        save_user_data(user_data)
        print(request.args.get('response'))
        return render_template('success.html')
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)