from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host='postgres-db',
        database='postgres',
        user='postgres',
        password='mysecretpassword'
    )
    return conn

@app.route('/order', methods=['POST'])
def create_order():
    order = request.json
    product_id = order['product_id']

    # Check product availability
    product_response = requests.get(f'http://product-service:5000/product/{product_id}')
    if product_response.status_code == 404:
        return "Product not found", 404

    # Process payment
    payment_response = requests.post('http://payment-service:5002/payment', json=order)
    if payment_response.status_code != 200:
        return "Payment failed", 400

    # Save order to database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (product_id, quantity) VALUES (%s, %s)', (product_id, order['quantity']))
    conn.commit()
    cur.close()
    conn.close()

    # Send notification
    notification_response = requests.post('http://notification-service:5003/notify', json={
        "message": f"Order for product {product_id} has been placed successfully."
    })
    if notification_response.status_code != 200:
        return "Failed to send notification", 500

    return jsonify({"message": "Order placed successfully!", "order": order}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
